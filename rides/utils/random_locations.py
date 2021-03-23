import random
import math
from urllib.parse import urlencode
import requests

class Location_Generator():

    API = "AIzaSyB8yOuNdpcUpjV3ilOJbrdZtrey9BHNStA"

    def random_radius(self, radius):
        u = random.random() + random.random()
        r = radius * (2 - u if u > 1 else u)
        return r

    def get_coor(self, loc):
        dis_ep = "https://maps.googleapis.com/maps/api/geocode/json"
        data = urlencode({"address": loc, "key": self.API})
        lookup_url = f"{dis_ep}?{data}"
        r = requests.get(lookup_url)
        data = r.json()["results"][0]["geometry"]["location"]
        print(data["lat"],",",data["lng"])

        return [data["lat"], data["lng"]]

    def convert_lat(self, dist):
        return dist/111

    def convert_lng(self, dist):
        return dist/111.321

    def random_points(self, radius, data):
        t = 2 * math.pi * random.random()
        print(t/math.pi)
        radius = self.random_radius(radius)
        print(radius)
        x = 111*data[0] + radius * math.cos(t)
        y = 111.321*data[1] + radius * math.sin(t)
        x = self.convert_lat(x)
        y = self.convert_lng(y)
        loc = [x, y]
        return loc

gg = Location_Generator()
data = gg.get_coor("Lido Mall, Bangalore") 
# print(gg.get_coor("Sai Poorna Heights, Bangalore"))
loc = (gg.random_points(1.8, data))
print(loc)
# print(requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(loc[0])+","+str(loc[1])+"&key=AIzaSyB8yOuNdpcUpjV3ilOJbrdZtrey9BHNStA").json())