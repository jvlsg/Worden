from .trackable_object import TrackableObject
import datetime as dt

def parse_net_launch_window(nw_str):
    #2019-10-09T22:25:00-03:00
    if type(nw_str) != str:
        return None

    return dt.datetime(
        int(nw_str[0:4]), #Year
        int(nw_str[5:7]), #Month
        int(nw_str[8:10]), #Day
        int(nw_str[11:13]), #Hour
        int(nw_str[14:16]), #Minute
        int(nw_str[17:19]) #Second
    )


class Launch(TrackableObject):
    def __init__(self, launch_json):
        self.name = launch_json["name"] or ""
        self.net_window = parse_net_launch_window(launch_json["net"])
        self.status = launch_json["status"]["name"] or ""
        
        """
        mission	
            id	25
            launch_library_id	1155
            name	"Cygnus CRS NG-12"
            description	"This is the 13th planned flight of the Orbital ATK's uncrewed resupply spacecraft Cygnus and its 12th flight to the International Space Station under the Commercial Resupply Services contract with NASA."
            type	"Resupply"
            orbit	"Low Earth Orbit"
            orbit_abbrev	"LEO"
        """
        self.mission = launch_json["mission"] or {"name":"N/A","type":"N/A","description":"N/A","orbit":"N/A"}

        self.pad = launch_json["pad"] or {}

    def __repr__(self):
        return """
        \nNAME: {}
        \nSTATUS: {}\tDATE: {} 
        \nMISSION: {}
        \tTYPE: {}
        \tORBIT: {}
        \nPAD: {}
        \tLOCATION: {}
        \nMISSION DETAILS: {}
        """.format(
            self.name,
            self.status, self.net_window,
            self.mission.get('name'),
            self.mission.get('type'),
            self.mission.get('orbit'),
            self.pad.get("name"),
            self.pad.get("location").get("name"),
            self.mission.get('description')
            )

    def __str__(self):
        return self.__repr__()

    def track(self):
        return float(self.pad["latitude"]),float(self.pad["longitude"])
