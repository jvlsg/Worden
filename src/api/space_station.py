from src.api.trackable_object import TrackableObject
from src.api.api_utils import parse_str_to_date
import datetime

class SpaceStation(TrackableObject):

    def __init__(self,station_json):
        self.name = station_json.get("name")
        self.status = station_json.get("status").get("name")
        self.type = station_json.get("type").get("name")
        self.description = station_json.get("description")
