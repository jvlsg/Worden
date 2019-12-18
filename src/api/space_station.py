from src.api.trackable_object import TrackableObject
from src.api.api_utils import parse_str_to_date
import datetime

class SpaceStation(TrackableObject):

    def __init__(self,station_json):
        self.name = station_json.get("name")
        self.status = station_json.get("status").get("name")
        self.orbit = station_json.get("orbit")
        self.type = station_json.get("type").get("name")
        self.description = station_json.get("description")
        self.founded_date = station_json.get("founded")
        self.global_coordinates = {"latitude":"","longitude":""}
        self.owners = ["{}({})".format(x.get("name"),x.get("abbrev")) for x in station_json.get("owners")]

    def __repr__(self):

        return """
        \nNAME: {}
        \nSTATUS: {}\tTYPE: {} 
        \nORBIT: {}\tCOORDS:{}
        \n{}
        \nFOUNDED: {}
        \nOWNERS: \n\t{}
        """.format(
            self.name,
            self.status, self.type,
            self.orbit,self.track_global_coordinates(),
            self.description,
            self.founded_date,
            "\n\t".join(self.owners)
            )

    def track_global_coordinates(self):
        return float(self.global_coordinates["latitude"]),float(self.global_coordinates["longitude"])
