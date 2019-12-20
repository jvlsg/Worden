from src.ui.ui_utils import TextBox, WordenForm
from src.api.api_man import Api_Page
import src.const as const
import npyscreen
import logging
import time
import requests

class ListAndDetailsForm(WordenForm):

    def create(self, *args, **keywords):
        
        super(ListAndDetailsForm, self).create(*args, **keywords)
        self.w_object_selection = self.add(npyscreen.BoxTitle, name="",
            values=[],
            max_width=40,
            rely=self.PADDING_Y,
            relx=self.PADDING_X,
        )
        self.w_object_selection.when_value_edited = self.update_launch_details
        self.selected_object = None

        self.w_object_details_box = self.add(TextBox,
            name="DETAILS",
            max_width= self.USEABLE_X-self.w_object_selection.max_width-5, 
            max_height = self.USEABLE_Y-3,
            #Relx of the previous + width of the previous - Padding 
            relx = self.w_object_selection.relx + self.w_object_selection.width - 2*self.PADDING_X, 
            rely=self.PADDING_Y,
            autowrap=True,
            footer="^T: Track"
            )       

    def set_api_type(self,api_type):
        """
        Sets the API type and populates the current API Page
        """
        if type(api_type) != const.API_TYPES:
            raise TypeError("{} not in API_TYPES".format(api_type))
        self.api_type = api_type
            
        try:
            npyscreen.notify("Fetching {}\nPlease Wait...".format(api_type.value),title="INTIALIZING",wide=True)
            self.parentApp.api_man.getters_dict.get(self.api_type)()
            self.api_page = self.parentApp.api_man.pages.get(self.api_type)
        except requests.exceptions.ConnectionError:
            npyscreen.notify_wait(const.MSG_CONNECTION_ERROR,title="Connection Error",form_color='WARNING')
            self.api_page = Api_Page()
            

    def update_launch_details(self):
        if type(self.w_object_selection.value) != int: #Sanity Check
            return
        
        #Get details of the current selected launch
        self.selected_object = self.api_page.results_dict.get(
            self.w_object_selection.values[self.w_object_selection.value])

        logging.debug("Selected Object {}".format(self.w_object_selection.values[self.w_object_selection.value]))
        self.w_object_details_box.value = str(self.selected_object)
        self.w_object_details_box.entry_widget.reformat_preserve_nl()
        self.w_object_details_box.display()        
        
    def track_object(self,*args,**keywords):
        if self.selected_object == None  : #Sanity Check
            return
        self.parentApp.set_tracked_object(
            trackable_object=self.selected_object,
            trackable_object_key=self.w_object_selection.values[self.w_object_selection.value],
            trackable_object_type=self.api_type)
        npyscreen.notify("Now Tracking {}".format(self.selected_object.name),title="Object Selected")
        time.sleep(1)

    def h_increment_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the next values
        """
        self.parentApp.api_man.getters_dict.get(self.api_type)(next_page=True)
        self.update_form()


    def h_decrement_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the previous values
        """
        self.parentApp.api_man.getters_dict.get(self.api_type)(next_page=False)
        self.update_form()

    def update_form(self):
        self.w_object_selection.values = list(self.api_page.results_dict.keys())
        self.w_object_selection.footer = "< {}/{} >".format(self.api_page.current_page_number,self.api_page.maximum_page_number)
        self.w_object_selection.update()
        self.update_launch_details()

    def while_waiting(self):
        try:
            self.parentApp.api_man.getters_dict[self.api_type]()
        except requests.exceptions.ConnectionError as e:
            npyscreen.notify_wait(const.MSG_CONNECTION_ERROR,title="Connection Error",form_color='WARNING')
        self.update_form()
