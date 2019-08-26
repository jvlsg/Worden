#!/usr/bin/env python
import npyscreen, curses
from src.ui.map_form import MapForm, HustonForm
from src.api import api_man
import logging
logging.basicConfig(filename="huston.log", level=logging.DEBUG)

class HustonApp(npyscreen.NPSAppManaged):
    """
    The core of Huston's Logic will be here.
    The Form classes should only know what is required to display themselves
    """

    def while_waiting(self):
        #UPDATE THE CURRENT FORM 
        self._Forms[self._active_form].update_form()
        ##TODO FETCH API ?
    
    def onStart(self):
        #THIS NEEDS TO BE BEFORE REGISTERING THE FORM 
        #ms between calling while_waiting
        self.keypress_timeout_default = 50

        #self.f_launches = SecForm(parentApp=self, name="LAUNCHES")
        self.f_map = MapForm(parentApp=self, name="MAPS")
        self.registerForm("MAIN",self.f_map)

        self.f_test = npyscreen.FormMutt(parentApp=self,name="aoigvoai")
        self.registerForm("LAUNCHES",self.f_test)


        self._active_form = "MAIN"
        
        ##TODO For Geo Location Tracking
        ##TODO Update positions/coordinates of trackable objects
        ## There are Objects In
        #self.update_obj_positions(...)
        self.tracked_object = None
        self.set_tracked_object()

        ##TODO Set Dictionaries for all data used by the Forms
    
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
        self.resetHistory()
    


