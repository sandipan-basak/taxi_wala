from urllib.parse import urlencode
import requests

class GoogleApiHandler:

    API = "AIzaSyB8yOuNdpcUpjV3ilOJbrdZtrey9BHNStA"
    def calculate_distance(self, orig, dest):
        dis_ep = "https://maps.googleapis.com/maps/api/distancematrix/json"
        data = urlencode({"origins": orig, "destinations": dest, "key": self.API})
        lookup_url = f"{dis_ep}?{data}"
        r = requests.get(lookup_url)
        return r.json()
