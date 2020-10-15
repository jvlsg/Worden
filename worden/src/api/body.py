from worden.src.api.trackable_object import TrackableObject
from worden.src.api.api_utils import parse_str_to_date
import datetime

class Body(TrackableObject):

    def __init__(self,body_json):
        self.name =  body_json.get("englishName")
        self.is_planet =  body_json.get("isPlanet")
        self.semimajorAxis = body_json.get("semimajorAxis")
        self.perihelion = body_json.get("perihelion")
        self.aphelion = body_json.get("aphelion")
        self.eccentricity = body_json.get("eccentricity")
        self.inclination = body_json.get("inclination")

        json_mass = body_json.get("mass")
        self.mass = ""
        if json_mass != None:
            self.mass = float("{}E{}".format(json_mass.get("massValue"),json_mass.get("massExponent")))

        json_vol = body_json.get("vol")
        self.vol = ""
        if json_vol != None:
            self.vol = float ("{}E{}".format(json_vol.get("volValue"),json_vol.get("volExponent")))
        self.density = body_json.get("density")
        self.gravity = body_json.get("gravity")
        self.escape = body_json.get("escape")
        self.mean_radius = body_json.get("meanRadius")
        self.equa_radius = body_json.get("equaRadius")
        self.polar_radius = body_json.get("polarRadius")
        self.flattening = body_json.get("flattening")
        self.sideral_orbit = body_json.get("sideralOrbit")
        self.sideral_rotation = body_json.get("sideralRotation")
        self.discovered_by = body_json.get("discoveredBy")
        self.discovery_date = body_json.get("discoveryDate")
        self.alternative_name = body_json.get("alternativeName")

    def __repr__(self):
        s = "{}".format(self.name)

        if self.alternative_name != "":
            s+= "\nALTERNATE NAME: {}".format(self.alternative_name)
        if self.is_planet:
            s += "\nPLANET\n"
        if self.discovered_by != "":
            s +="\nDISCOVERED BY: {} on {}".format(self.discovered_by,self.discovery_date)
        
        s += """\nAPHELION:{} km\t|\tPERIHELION:{} km
        \nSEMI-MAJOR AXIS: {} m
        \nECC: {}|\tINC: {}°
        \nMASS: {} kg|\tVOLUME: {}|\tDENSITY: {} kg/m^3
        \nGRAVITY: {} m/s^2|\tESCAPE VELOCITY: {} km/s
        \nMEAN RADIUS: {} km |\tFLATTENING: {}
        \n\tEQUATOR RADIUS: {} km|\tPOLAR RADIUS: {} km
        \nSIDERAL ORBIT: {} days|\tSIDERAL ROTATION: {} hours
        """.format(
            self.perihelion,
            self.aphelion,
            self.semimajorAxis,
            self.eccentricity,
            self.inclination,
            self.mass,
            self.vol,
            self.density,
            self.gravity,
            self.escape,
            self.mean_radius,
            self.flattening,
            self.equa_radius,
            self.polar_radius,
            self.sideral_orbit,
            self.sideral_rotation
            )
            
        return s
