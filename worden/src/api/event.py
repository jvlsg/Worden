from worden.src.api.trackable_object import TrackableObject
from worden.src.api.api_utils import parse_str_to_date
import datetime

class Event(TrackableObject):
    
    def __init__(self,event_json):
        self.name = event_json.get("name")
        self.type = event_json.get("type").get("name")
        self.description = event_json.get("description")
        self.date = event_json.get("date")
        self.location = event_json.get("location")

        self.news_url = event_json.get("news_url")
        if self.news_url == None:
            self.news_url = ""

        self.launches=[]
        for l in event_json.get("launches"):
            self.launches.append(l.get("name"))

        self.spacestations = []
        for s in event_json.get("spacestations"):
            self.spacestations.append(s.get("name"))

    def __repr__(self):
        return """NAME: {}\t TYPE: {}
        \nDATE: {}\tLOCATION: {}
        \n{}
        \nLAUNCHES: {}
        \nSPACE STATIONS: {}
        \nNEWS URL:{}
        """.format(self.name,self.type,self.date,self.location,self.description,"\n\t".join(self.launches),"\n\t".join(self.spacestations),self.news_url)