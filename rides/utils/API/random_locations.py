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
        url = urlencode({"address": loc, "key": self.API})
        lookup_url = f"{dis_ep}?{url}"
        r = requests.get(lookup_url)
        req = r.json()["results"][0]["geometry"]["location"]
        return [req["lat"], req["lng"]]

    def convert_lat(self, dist):
        return dist/111

    def convert_lng(self, dist):
        return dist/111.321

    def random_points(self, radius, data):
        t = 2 * math.pi * random.random()
        radius = self.random_radius(radius)
        x = self.convert_lat(111*data[0] + radius * math.cos(t))
        y = self.convert_lat(111.321*data[1] + radius * math.sin(t))
        return [x, y]

# gg = Location_Generator()
# data = gg.get_coor("Lido Mall, Bangalore")
# loc = (gg.random_points(1.8, data))
# print(loc)
