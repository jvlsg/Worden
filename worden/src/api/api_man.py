import requests
import worden.src.const as const
from .launch import Launch
from .astronaut import Astronaut
from .space_station import SpaceStation
from .event import Event
from .body import Body
from pprint import pprint
import logging
from collections import OrderedDict
"""
Provides functions that call / parse / format data from the multiple apis
"""

class Api_Manager():
    """
    Class that manages variables and provides methods to fetch the APIs 
    """

    def __init__(self,app):
        self.app = app
        self.pages = {
            const.API_TYPES.LAUNCHES: Api_Page(),
            const.API_TYPES.ASTRONAUTS: Api_Page(),
            const.API_TYPES.SPACE_STATIONS: Api_Page(),
            const.API_TYPES.EVENTS: Api_Page(),
            const.API_TYPES.SOLAR_SYSTEM_BODIES: Api_Page(offset_delta=1)
        }
        
        # Dict of Functions that get data using the api
        self.getters_dict = {
            const.API_TYPES.LAUNCHES:self.get_upcoming_launches,
            const.API_TYPES.ASTRONAUTS:self.get_astronauts,
            const.API_TYPES.SPACE_STATIONS:self.get_space_stations,
            const.API_TYPES.EVENTS:self.get_events,
            const.API_TYPES.SOLAR_SYSTEM_BODIES: self.get_solar_system_bodies
        }

    def get_solar_system_bodies(self,next_page=None):
        url = "https://api.le-systeme-solaire.net/rest.php/bodies?page={}"
        self.update_api_page(self.pages[const.API_TYPES.SOLAR_SYSTEM_BODIES],next_page,url,"englishName",Body,list_key="bodies")

    def get_events(self,next_page=None):
        url = "https://spacelaunchnow.me/api/3.3.0/event/upcoming/?format=json&offset={}"
        self.update_api_page(self.pages[const.API_TYPES.EVENTS],next_page,url,"name",Event)

    def get_astronauts(self,next_page=None):
        """
        Gets upcoming launches, updates paging
        Args:
            next: Boolean, gets the next page of objects if True. Gets the previous if False. Gets of the same page if None
        Returns:
            The resullting Api Page
        """
        url = "https://spacelaunchnow.me/api/3.3.0/astronaut/?&offset={}&status=1"
        self.update_api_page(self.pages[const.API_TYPES.ASTRONAUTS],next_page,url,"name",Astronaut)

    def get_upcoming_launches(self,next_page=None):
        """
        Gets upcoming launches, updates paging
        Args:
            next: Boolean, gets the next page of objects if True. Gets the previous if False
        Returns:
            The resullting Api Page
        """
        url = "https://spacelaunchnow.me/api/3.3.0/launch/upcoming/?format=json&offset={}"
        self.update_api_page(self.pages[const.API_TYPES.LAUNCHES],next_page,url,"name",Launch)

    def get_space_stations(self,next_page=None):
        page = self.pages[const.API_TYPES.SPACE_STATIONS] # ref
        url = "https://spacelaunchnow.me/api/3.3.0/spacestation/?format=json&status=1&offset={}"
        self.update_api_page(page,next_page,url,"name",SpaceStation)
        
        #Get current ISS location
        if "International Space Station" in page.results_dict.keys():            
            json_results = request_json("http://api.open-notify.org/iss-now.json")
            iss_position = json_results["iss_position"]
            page.results_dict["International Space Station"].global_coordinates["latitude"] = iss_position["latitude"]
            page.results_dict["International Space Station"].global_coordinates["longitude"] = iss_position["longitude"]

    def update_api_page(self,page=None,next_page=None,url="",dict_key_key=None,object_type=None,list_key="results"):
        """
        Updates the contents of an API Page

        Args:
            page: Api_Page object
            next: Boolean, gets the next page of objects if True. Gets the previous if False
            url: Url to request JSON objects with {} properly placed to input the updated offset
            dict_key_key: The key that will be used as the key for the dict of objects
            object_type: Class of the objects that will be the values of the dict
            list_key: Key to access the list of JSONs of the object type. "results" by default
            is_ordered_dict: Boolean, to use or no an oredered dict for the page
        """
        #Sanity Check
        if type(page) != Api_Page:
            return True

        if type(next_page) == bool:
            page_flip_result = False
            if next_page:
                page_flip_result = page.next_page()
            else:
                page_flip_result = page.previous_page()
            if not page_flip_result:
                return True

        json_results = request_json(url.format(page.current_offset))
        page.results_dict = {e.get(dict_key_key): object_type(e) for e in json_results.get(list_key)}

        count = json_results.get("count")
        if count != None:
            page.count = count
        else:
            page.count = 1
        
        return True

def request_json(url=""):
    """
    Generic function that does an API request for a JSON object
    Args:
        url: request URL
    Returns:
        JSON object if successful
        None otherwise
    """
    try:
        logging.debug("Getting {}".format(url))
        r = requests.get(url)
        return r.json()
    except requests.exceptions.ConnectionError as e:
        logging.error("Unable to Connect to {}".format(url))
        raise e
        


class Api_Page():
    """
    Controls the last accessed "page" of the API
    Buffers the results of the Api requests, Tracks the offset for future requests
    """
    def __init__(self,offset_delta = const.DEFAULT_OFFSET_DELTA):
        self.offset_delta = offset_delta
        self.count = 0 #Count of Items available
        self.current_offset = 0
        self.maximum_offset = 1000

        # Page Number based on the Offset and Maximum number of objects
        self.current_page_number = 1
        self.maximum_page_number = 1
        self.results_dict = {} #Currently buffered Results

    def next_page(self):
        """
        Increments the current offset with offset delta. 
        Returns True if successful, Returns False otherwise
        """
        modded_offset = self.current_offset + self.offset_delta
        if modded_offset <= self.maximum_offset:
            self.current_page_number+=1
            self.current_offset = modded_offset
            return True
        return False

    def previous_page(self):
        """
        Decrements the current offset with offset delta. 
        Returns True if successful, Returns False otherwise
        """
        modded_offset = self.current_offset - self.offset_delta
        if modded_offset >= 0 :
            self.current_offset = modded_offset
            self.current_page_number-=1
            return True
        return False
    
    @property
    def count(self):
        return self.count
    @count.setter
    def count(self,new_count):
        self.maximum_offset = new_count - self.offset_delta
        self._count = new_count
        self.maximum_page_number = int(self.maximum_offset/self.offset_delta)+1
