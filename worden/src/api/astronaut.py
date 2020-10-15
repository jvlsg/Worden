from worden.src.api.trackable_object import TrackableObject
from worden.src.api.api_utils import parse_str_to_date
import datetime

class Astronaut(TrackableObject):

    def __init__(self,astronaut_json):
        self.name = astronaut_json.get("name")
        self.status = astronaut_json.get("status").get("name")
        self.type = astronaut_json.get("type").get("name")
        self.date_of_birth = datetime.date.fromisoformat(astronaut_json.get("date_of_birth"))
        if astronaut_json.get("date_of_death") != None:
            self.date_of_death = datetime.date.fromisoformat(astronaut_json.get("date_of_death"))
        self.nationality = astronaut_json.get("nationality")
        self.bio = astronaut_json.get("bio")
        self.twitter = astronaut_json.get("twitter")
        self.instagram = astronaut_json.get("instagram")
        self.wiki = astronaut_json.get("wiki")
        if astronaut_json.get("agency") != None:
            self.agency = astronaut_json.get("agency")
        else:
            self.agency = "N/A"
        self.profile_image = astronaut_json.get("profile_image")

    def __repr__(self):
        return """
        \nNAME: {}
        \nSTATUS: {}
        \nAGENCY: {} ({}) | {}
        \nBIO: 
        \nDate Of Birth: {}
        \n{}
        \nSOCIAL:
        \n Wiki: {}
        \n Twitter: {}
        \n Instagram: {}
        """.format(
            self.name,
            self.status,
            self.agency.get("name"),self.agency.get("abbrev"),self.agency.get("type"),
            self.date_of_birth,
            self.bio,
            self.wiki,self.twitter,self.instagram)

    def track_global_coordinates(self):
        return None