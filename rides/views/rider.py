import time
from  datetime import datetime
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils import timezone
from background_task import background
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView

from rides.utils.google_api_util import GoogleApiHandler
from rides.utils.random_locations import Location_Generator
from rides.utils.s2_get_cap import GetCap
from ..decorators import rider_required
from ..forms import RiderSignUpForm, BookRideViewForm
from ..models import Status, User, Ride, Executive, Cab


class RiderSignUp(CreateView):
    model = User
    form_class = RiderSignUpForm
    template_name = 'registration/signup_form.html'

    gAPI = GoogleApiHandler()
    cap = GetCap()
    gL = Location_Generator()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_type'] = 'rider'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('rider:book')

@method_decorator([login_required, rider_required], name='dispatch')
class SetLocation(CreateView):
    model = Ride
    form_class = BookRideViewForm
    template_name = 'rides/rider/get_ride.html'

    gAPI = GoogleApiHandler()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_oq = Status.objects.get(name="On Queue").ride_set.all()
        status_og = Status.objects.get(name="Ongoing").ride_set.all()
        onqueue_ride = status_oq.filter(rider=self.request.user).first()
        ongoing_ride = status_og.filter(rider=self.request.user).first()
        print(onqueue_ride)
        print(ongoing_ride)
        if not onqueue_ride and not ongoing_ride:
            context["ride_flag"] = 0
            context["r_pk"] = 1
        elif not ongoing_ride:
            context["ride_flag"] = 1
            context["r_pk"] = onqueue_ride.pk
        else:
            context["ride_flag"] = 2
            context["r_pk"] = ongoing_ride.pk
        print(context["ride_flag"])
        print(context["r_pk"])
        return context
    
    def give_active_shifts(self, time):
        UTC_m_time = datetime.strptime("02:30:00", "%H:%M:%S")
        UTC_me_time = datetime.strptime("11:30:00", "%H:%M:%S")
        UTC_e_time = datetime.strptime("10:30:00", "%H:%M:%S")
        UTC_ee_time = datetime.strptime("19:30:00", "%H:%M:%S")
        UTC_n_time = datetime.strptime("18:30:00", "%H:%M:%S")
        UTC_ne_time = datetime.strptime("03:30:00", "%H:%M:%S")
        if UTC_m_time < time < UTC_me_time:
            status = "M"
        if UTC_e_time < time < UTC_ee_time:
            status = "E" if not status else status+"E"
        if UTC_n_time < time < UTC_ne_time:
            status = "N" if not status else status+"N"
        return status
        
    def form_valid(self, form):
        ride = form.save(commit=False)
        ride_status = Status.objects.get(name="On Queue")
        ride.status = ride_status
        ride.rider = self.request.user
        
        data = self.gAPI.calculate_distance(orig=ride.source, dest=ride.destination)
        ride.travelled = int(data['rows'][0]['elements'][0]['distance']['value'])/1000
        total_duration = data['rows'][0]['elements'][0]['duration']['value']
        ride.charges = self.gAPI.calculate_cost(ride.travelled, total_duration)
        ride.save()
        partners = Executive.objects.filter(is_engaged=False)
        for x in self.give_active_shifts(ride.date_time):
            queryset = partners.filter(shift=x)
            if not cabees:
                cabees = queryset
            else:
                cabees.union(queryset)
        # Create random cab locations in the city
        for cabee in cabees:
            random_loc = gL.random_points(10, gL.get_coor(ride.source))
            cabee.car.lat = random_loc[0]
            cabee.car.lng = random_loc[1]
            cabee.car.save()

        get_cabs(ride, cabee_list, 200, schedule=timezone.now())
        return redirect('rider:live', ride.pk)

        # Initiate randome location creation
        status_string = self.give_active_shifts(ride.date_time)
        for i in st:
            if not cabees:
                cabees = Executive.objects.filter(shift=i)
            else:
                cabees.union(Executive.objects.filter(shift=i))
        cabees = cabees.filter(is_engaged=False)
        
        random_locations(ride, 6000, status_string, cabees, schedule=timezone.now())
        get_close_cabs(ride, cabees, schedule=timezone.now())

        # create_car_posititons(ride.source, Executive.objects.filter(e.date_time))

@background
def get_cabs(self, ride, cabees, radius):
    cap = GetCap()
    while(True):
        region = cap.find_cover(radius, ride.source)
        close_by_cabs = []
        for cabee in cabees:
            if cap.contains([cabee.car.lat, cabee.car.lng], region):
                close_by_cabees.append(cabee)
        for cabee in close_by_cabees:
            ride.cab = cabee.cab
            ride.cabee = cabee
            ride.save()
            cabee.is_engaged = True
            old.is_engaged = False
            old.save()
            print(ride.cabee.user.name)
            time.sleep(60)
            old = cabee

        radius = radius + 100

        if radius > 4500:
            break
    

@background
def random_locations(ride, radius, st, cabees):
    g_l = Location_Generator()
    for i in st:
        if not cabees:
            cabees = Executive.objects.filter(shift=i)
        else:
            cabees.union(Executive.objects.filter(shift=i))
    cabees = cabees.filter(is_engaged=False)
    
    for cabee in cabees:
        curr_loc = g_l.random_points(radius, g_l.get_coor(ride.source))
        cabee.car.lat = curr_loc[0]
        cabee.car.lng = curr_loc[1]
        cabee.car.save() 

@background
def get_close_cabs(ride, cabees):
    s2_cap = GetCap()
    rad = 150
    while True:
        s2_cap.find_cover(150, Location_Generator.get_coor(ride.source))

        for cabee in cabees:
            if s2_cap.contains([cabee.car.lat, cabee.car.lng]):
                ride.cabee = cabee
                ride.status = Status(name="Ongoing")
                

        rad = rad + 100    
        if rad > 4000:
            break
    

@method_decorator([login_required, rider_required], name='dispatch')
class BookRide(DetailView):
    model = Ride
    template_name = 'rides/rider/check_ride.html'
    gAPI = GoogleApiHandler()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ride = self.get_object()
        context['rider'] = ride.rider
        context['cab'] = ride.cab
        context['cabee'] = ride.cabee
        return context

@method_decorator([login_required, rider_required], name='dispatch')
class RideView(DetailView):
    model = Ride
    context_object_name = 'ride'
    template_name = 'rides/rider/ride_status.html'

    def get_context_data(self, **kwargs):
        kwargs['rider'] = self.get_object().rider
        
        kwargs['cabee'] = self.get_object().cabee

        return super().get_context_data(**kwargs)

@method_decorator([login_required, rider_required], name='dispatch')
class PastRides(ListView):
    model = Ride
    
    def get_queryset(self, **kwargs):
        rider = self.request.user.rider
        queryset = Ride.objects.filter(rider=rider)
        return queryset

# @login_required
# @rider_required
# def update_ride(request, pk):
    
