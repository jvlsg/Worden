import requests
import src.const as const
from .launch import Launch
from pprint import pprint
import logging
import enum

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
            const.API_TYPES.LAUNCHES: Api_Page()
        }


    def get_upcoming_launches(self,next_page=True):
        """
        Gets upcoming launches, updates paging
        Args:
            next: Boolean, gets the next page of objects if True. Gets the previous if False
        Returns:
            The new Dict of Launch objects (new data was fetched) or the current 
        """
        page = self.pages[const.API_TYPES.LAUNCHES] # ref
        page_flip_result = False
        if next_page:
            page_flip_result = page.next_page()
        else:
            page_flip_result = page.previous_page()

        if not page_flip_result:
            return page.results_dict

        res = request_json(
            "https://spacelaunchnow.me/api/3.3.0/launch/upcoming/?format=json&offset={}".format(
                page.current_offset)
            )
        
        launch_dict = {e["name"]: Launch(e) for e in res["results"]}

        #Updates the page data
        page.results_dict = launch_dict
        page.count = res["count"]
        return page.results_dict

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
        r = requests.get(url)
        return r.json()
    except:
        return None


class Api_Page():
    """
    Controls the last accessed "page" of the API
    Buffers the results of the Api requests, Tracks the offset for future requests
    """
    def __init__(self):
        self.count = 0
        self.current_offset = -const.OFFSET_DELTA
        self.maximum_offset = const.OFFSET_DELTA
        self.results_dict = {}

    def next_page(self):
        """
        Increments the current offset with offset delta. 
        Returns True if successful, Returns False otherwise
        """
        modded_offset = self.current_offset + const.OFFSET_DELTA
        if modded_offset <= self.maximum_offset:
            self.current_offset = modded_offset
            return True
        return False

    def previous_page(self):
        """
        Decrements the current offset with offset delta. 
        Returns True if successful, Returns False otherwise
        """
        modded_offset = self.current_offset - const.OFFSET_DELTA
        if modded_offset >= 0 :
            self.current_offset = modded_offset
            return True
        return False
    

    @property
    def count(self):
        return self.count
    @count.setter
    def count(self,new_count):
        self.maximum_offset = new_count - const.OFFSET_DELTA
        self._count = new_count