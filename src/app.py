#!/usr/bin/env python
import curses
import logging

import npyscreen

from src.api import api_man
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
    
    def onStart(self):
        #THIS NEEDS TO BE BEFORE REGISTERING THE FORM 
        #ms between calling while_waiting
        self.keypress_timeout_default = 25


        self.api_man = api_man.Api_Manager(self)
        
        # Dict of Functions that get data using the api
        self.api_getters_dict = {
            const.API_TYPES.LAUNCHES:self.api_man.get_upcoming_launches,
            const.API_TYPES.ASTRONATUS:self.api_man.get_astronatus
        }

        self.f_map = MapForm(parentApp=self, name="MAPS")
        self.registerForm("MAIN",self.f_map)

        self.f_launches = ListAndDetailsForm(parentApp=self,name="LAUNCHES")
        self.f_launches.set_api_type(const.API_TYPES.LAUNCHES)
        self.registerForm(const.API_TYPES.LAUNCHES,self.f_launches)

        self.f_astronatus = ListAndDetailsForm(parentApp=self,name="ASTRONAUTS")
        self.f_astronatus.set_api_type(const.API_TYPES.ASTRONATUS)
        self.registerForm(const.API_TYPES.ASTRONATUS,self.f_astronatus)
        

        self._active_form = "MAIN"
        ##TODO For Geo Location Tracking
        ##TODO Update positions/coordinates of trackable objects
        ## There are Objects In
        #self.update_obj_positions(...)
        self.tracked_object = None


    def set_tracked_object(self,trackable_object):
        """
        Sets the new tracked object and invokes the mapForm
        method to draw it
        """
        logging.debug("Set Tracked Object to: {}".format(trackable_object))
        self.tracked_object = trackable_object

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
