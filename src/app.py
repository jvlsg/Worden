#!/usr/bin/env python
import curses
import logging

import npyscreen

from src.api import api_man
from src.api.trackable_object import TrackableObject
from src.ui.list_and_details_form import ListAndDetailsForm
from src.ui.map_form import MapForm
import src.const as const
logging.basicConfig(filename="worden.log", level=logging.DEBUG)

class WordenApp(npyscreen.NPSAppManaged):
    """
    The core of the application's Logic will be here.
    The Form classes should only know what is required to display themselves
    """

    def while_waiting(self):
        #UPDATE THE CURRENT FORM
        self._Forms[self._active_form].update_form()

        if self.tracked_object != None and self._active_form != self.tracked_object_type:
            #Invokes the while_waiting , which will in turn update the list of objects
            self._Forms[self.tracked_object_type].while_waiting()
            #Gets the equivalent to the tracked object again
            self.tracked_object = self.api_man.pages.get(self.tracked_object_type).results_dict.get(self.tracked_object_key)
    
    def onStart(self):
        #THIS NEEDS TO BE BEFORE REGISTERING THE FORM 
        self.keypress_timeout_default = const.KEYPRESS_TIMEOUT

        self.api_man = api_man.Api_Manager(self)

        self.f_map = MapForm(parentApp=self, name="MAPS")
        self.registerForm("MAIN",self.f_map)

        self.f_launches = ListAndDetailsForm(parentApp=self,name="NEXT LAUNCHES")
        self.f_launches.set_api_type(const.API_TYPES.LAUNCHES)
        self.registerForm(const.API_TYPES.LAUNCHES,self.f_launches)

        self.f_ASTRONAUTS = ListAndDetailsForm(parentApp=self,name="ACTIVE ASTRONAUTS")
        self.f_ASTRONAUTS.set_api_type(const.API_TYPES.ASTRONAUTS)
        self.registerForm(const.API_TYPES.ASTRONAUTS,self.f_ASTRONAUTS)
        
        self.f_STATION = ListAndDetailsForm(parentApp=self,name="ACTIVE SPACE STATIONS")
        self.f_STATION.set_api_type(const.API_TYPES.SPACE_STATIONS)
        self.registerForm(const.API_TYPES.SPACE_STATIONS,self.f_STATION)


        self._active_form = "MAIN"
        self.tracked_object = None
        self.tracked_object_key = None
        self.tracked_object_type = None


    def set_tracked_object(self,trackable_object=None,trackable_object_key=None,trackable_object_type=None):
        """
        Sets the new tracked object, it's key and API Type
        """

        if not issubclass(type(trackable_object),TrackableObject) or trackable_object_key == None or trackable_object_type == None:
            raise TypeError()
        logging.debug("Set Tracked Object to a {}: {}".format(type(trackable_object),trackable_object_key))
        self.tracked_object = trackable_object
        self.tracked_object_key = trackable_object_key
        self.tracked_object_type = trackable_object_type

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def change_form_to(self, form_name):
        """
        Changes the App's current active form 
        """

        if form_name not in self._Forms.keys():
            return
        self._active_form = form_name
        self.switchForm(form_name)
        self._Forms[self._active_form].update_form()
        self.resetHistory()
