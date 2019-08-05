#!/usr/bin/env python
import npyscreen, curses
from src.ui.map_form import MapForm

class HustonApp(npyscreen.NPSAppManaged):

    def while_waiting(self):
        #UPDATE THE CURRENT FORM / FETCH API 
        pass
    
    def onStart(self):
        #THIS NEEDS TO BE BEFORE REGISTERING THE FORM 
        self.keypress_timeout_default = 10

        #self.f_launches = SecForm(parentApp=self, name="LAUNCHES")
        self.f_map = MapForm(parentApp=self, name="MAPS")
        self.registerForm("MAIN",self.f_map)

        self.test = npyscreen.FormMutt(parentApp=self,name="aoigvoai")
        self.registerForm("SECONDARY",self.test)


        self._current_active_form = "MAIN"
        
        ##TODO For Geo Location Tracking
        #self.current_tracked_obj

        ##TODO Set Dictionaries for all data used by the Forms

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")
    
    def change_form_to(self, form_name):
        """
        Changes the App's current active form 
        """

        if form_name not in self._Forms.keys():
            return
        self._current_active_form = form_name
        self.switchForm(form_name)
        self.resetHistory()
    


