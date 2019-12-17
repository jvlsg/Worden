from src.ui.ui_utils import TextBox, WordenForm
from src.api.api_man import Api_Page
import src.const as const
import npyscreen
import logging
import time

class ListAndDetailsForm(WordenForm):

    def create(self, *args, **keywords):
        
        super(ListAndDetailsForm, self).create(*args, **keywords)

        self.w_launch_selection = self.add(npyscreen.BoxTitle, name="",
            values=[],
            max_width=40,
            rely=self.PADDING_Y,
            relx=self.PADDING_X,
            #footer="< {}/{} >".format(self.api_page.current_page_number,self.api_page.maximum_page_number)
        )
        self.w_launch_selection.when_value_edited = self.update_launch_details
        self.selected_launch = None

        self.w_launch_details_box = self.add(TextBox,
            name="DETAILS",
            max_width= self.USEABLE_X-self.w_launch_selection.max_width-5, 
            max_height = self.USEABLE_Y-3,
            #Relx of the previous + width of the previous - Padding 
            relx = self.w_launch_selection.relx + self.w_launch_selection.width - 2*self.PADDING_X, 
            rely=self.PADDING_Y,
            autowrap=True,
            footer="^T: Track"
            )       

    def set_api_type(self,api_type):
        self.api_type = api_type
        self.api_page = self.parentApp.api_man.getters_dict[self.api_type](next_page=True)

    def update_launch_details(self):
        if type(self.w_launch_selection.value) != int: #Sanity Check
            return
        
        #Get details of the current selected launch
        self.selected_launch = self.api_page.results_dict.get(
            self.w_launch_selection.values[self.w_launch_selection.value])

        logging.debug("Selected Object {}".format(self.w_launch_selection.values[self.w_launch_selection.value]))
        self.w_launch_details_box.value = str(self.selected_launch)
        self.w_launch_details_box.entry_widget.reformat_preserve_nl()
        self.w_launch_details_box.display()        
        
    def track_object(self,*args,**keywords):
        if self.selected_launch == None  : #Sanity Check
            return
        self.parentApp.set_tracked_object(self.selected_launch)
        npyscreen.notify("Now Tracking {}".format(self.selected_launch.name))
        time.sleep(1)

    def h_increment_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the next values
        """
        self.api_page = self.parentApp.api_man.getters_dict.get(self.api_type)(next_page=True)
        self.update_form()


    def h_decrement_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the previous values
        """
        self.api_page = self.parentApp.api_man.getters_dict.get(self.api_type)(next_page=False)
        self.update_form()

    def update_form(self):
        self.w_launch_selection.values = list(self.api_page.results_dict.keys())
        self.w_launch_selection.footer = "< {}/{} >".format(self.api_page.current_page_number,self.api_page.maximum_page_number)
        self.w_launch_selection.update()