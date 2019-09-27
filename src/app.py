#!/usr/bin/env python
import curses
import logging

import npyscreen

from src.api import api_man
from src.ui.launches_form import LaunchesForm
from src.ui.map_form import MapForm

logging.basicConfig(filename="huston.log", level=logging.DEBUG)

class HustonApp(npyscreen.NPSAppManaged):
    """
    The core of Huston's Logic will be here.
    The Form classes should only know what is required to display themselves
    """

    def while_waiting(self):
        #UPDATE THE CURRENT FORM 
        self._Forms[self._active_form].update_form()
    
    def onStart(self):
        #THIS NEEDS TO BE BEFORE REGISTERING THE FORM 
        #ms between calling while_waiting
        self.keypress_timeout_default = 50

        self.f_map = MapForm(parentApp=self, name="MAPS")
        self.registerForm("MAIN",self.f_map)

        self.f_launches = LaunchesForm(parentApp=self,name="LAUNCHES")
        self.registerForm("LAUNCHES",self.f_launches)

        self._active_form = "MAIN"

        self.api_man = api_man.Api_Manager(self)

        ##TODO For Geo Location Tracking
        ##TODO Update positions/coordinates of trackable objects
        ## There are Objects In
        #self.update_obj_positions(...)
        self.tracked_object = None
        self.set_tracked_object()

        ##Dictionaries for all data used by the Forms
        self.data_dict = {
            "launches":self.api_man.get_upcoming_launches() #List
        }
    
    def set_tracked_object(self):
        """
        Sets the new tracked object and invokes the mapForm
        method to draw it
        """
        #self.tracked_object = api_man.get_iss_position()
        self.f_map.update_form()

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
