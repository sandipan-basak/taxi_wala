from time import sleep
from background_task import background
from rides.utils.google_api_util import GoogleApiHandler
from rides.utils.random_locations import Location_Generator
from rides.utils.s2_get_cap import GetCap
from ..models import User, Ride, Executive, Status
from django.utils import timezone


@background(schedule=0)
def random_locations(pk, st):
    gAPI = GoogleApiHandler()
    radius = 1.0
    ride = Ride.objects.get(id=pk)
    cabees = Executive.objects.all()
    g_l = Location_Generator()
    for i in st:
        if not cabees:
            cabees = Executive.objects.filter(shift=i)
        else:
            cabees.union(Executive.objects.filter(shift=i))
    cabees = cabees.filter(is_engaged=False)
    source_coor = g_l.get_coor(ride.source)
    
    for cabee in cabees:
        curr_loc = g_l.random_points(radius, source_coor)
        cab_road = gAPI.get_nearest_road([curr_loc[0], curr_loc[1]])
        cabee.car.lat = cab_road[0]
        cabee.car.lng = cab_road[1]
        cabee.car.save()
        print(cab_road[0], cab_road[1])
    get_close_cabs(pk, st, schedule=timezone.now())

@background(schedule=0)
def get_close_cabs(pk, st):
    print('Task starterd')
    rad = 300
    ride = Ride.objects.get(id=pk)
    cabees = Executive.objects.all()
    s2_cap = GetCap()
    gAPI = GoogleApiHandler()
    loc = Location_Generator()
    for i in st:
        if not cabees:
            cabees = Executive.objects.filter(shift=i)
        else:
            cabees.union(Executive.objects.filter(shift=i))
    cabees = cabees.filter(is_engaged=False)
    region = s2_cap.find_cover(rad, loc.get_coor(ride.source))
    while True:
        region = s2_cap.find_cover(rad, loc.get_coor(ride.source)) 
        for cabee in cabees:
            print(cabee.user.username)
            print("location:", cabee.car.lat, cabee.car.lng)
            print("rad", rad)
            print(region)
            if s2_cap.has([cabee.car.lat, cabee.car.lng], region):
                ride.cabee = cabee
                # ride.status = Status(name="Ongoing")
                ride.save()
                # Waiting for cabee to accept
                if ride.status == Status.objects.get(name="On Queue") and cabee.is_engaged == False:
                    print("engaged?", cabee.is_engaged)
                    c = 1
                    while True:
                        if cabee.is_engaged:
                            break
                        c = c + 1
                        print("waiting for ride acceptance...")
                        if c > 120:
                            break
                        sleep(1)
                # Partner accepts the ride
                if ride.status == Status.objects.get(name="Ongoing") and cabee.is_engaged == True:
                    origin = str(cabee.car.lat) + ',' + str(cabee.car.lng)
                    req_time = gAPI.calculate_distance(orig=origin, dest=ride.source)
                    dur = int(req_time['rows'][0]['elements'][0]['duration']['value']/60)
                    cab_reached = gAPI.get_nearest_road(loc.get_coor(ride.source))
                    time = timezone.now()
                    while True:
                        sleep(5)
                        curr = timezone.now()
                        # if rider cancels the ride.
                        if ride.status == Status.objects.get(name="Cancelled"):
                            return
                        # if partner cancels the ride.
                        if ride.status == Status.objects.get(name="On Queue"):
                            p_cancelled = True
                            break
                        time_diff = curr.minute - ride.updated_time.minute
                        time_diff = time_diff + 60 if time_diff < 0 else time_diff
                        if time_diff >= dur:
                            ride.is_started = True
                            ride.save()
                            ride.cab.lat = cab_reached[0]
                            ride.cab.lng = cab_reached[1]
                            ride.cab.save()
                            cabee.reached_loc == True
                            cabee.save()
                            break
                        else:
                            continue
                    # go for the next available partner
                    if p_cancelled:
                        break
            if ride.is_started:
                break
        rad = rad + 100
        if rad > 4000:
            break