import requests
from .launch import Launch
from pprint import pprint
import logging
"""
Provides functions that call / parse / format data from the multiple apis
"""

class Api_Manager():
    """
    Class that manages variables and provides methods to fetch the APIs 
    """

    def __init__(self,app):
        self.app = app

        self.api_offsets = {
            "upcoming_launches":0
        }

    def get_upcoming_launches(self,offset=0):
        """
        Returns Dict of Launch Objects for the upcoming launches
        """
        res = request_json(
            "https://spacelaunchnow.me/api/3.3.0/launch/upcoming/?format=json&offset={}".format(offset))
        
        launch_dict = {e["name"]: Launch(e) for e in res["results"]}
        return launch_dict
        

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