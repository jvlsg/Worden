from .trackable_object import TrackableObject

class Launch(TrackableObject):
    def __init__(self, launch_json):
        self.name = launch_json["name"] or ""
        self.window_start = launch_json["window_start"] or ""
        self.window_end = launch_json["window_end"] or ""
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
        \nMISSION: {} 
        \n\tTYPE: {}
        \n\tORBIT: {}
        \nPAD: {}
        \n\t LOCATION:{}
        \nDETAILS: {}
        """.format(
            self.name,
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
        return self.pad["latitude"],self.pad["longitude"],self
