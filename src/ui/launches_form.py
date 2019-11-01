from src.ui.ui_utils import TextBox, HustonForm
import src.const as const
import npyscreen
import logging
import time

class LaunchesForm(HustonForm):
    def create(self, *args, **keywords):
        super(LaunchesForm, self).create(*args, **keywords)

        self.api_type = const.API_TYPES.LAUNCHES

        self.launch_object_dict = self.parentApp.api_getters_dict[const.API_TYPES.LAUNCHES]()

        self.w_launch_selection = self.add(npyscreen.BoxTitle, name="",
            values=[],
            max_width=40,
            rely=self.PADDING_Y,
            relx=self.PADDING_X,
            footer="<: Prev {}\t>: Next {}".format(const.OFFSET_DELTA,const.OFFSET_DELTA)
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

    def update_launch_details(self):
        if type(self.w_launch_selection.value) != int: #Sanity Check
            return
        
        #Get details of the current selected launch
        self.selected_launch = self.launch_object_dict.get(
            self.w_launch_selection.values[self.w_launch_selection.value])

        logging.debug("Selected Launch {}".format(self.w_launch_selection.values[self.w_launch_selection.value]))
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
        self.launch_object_dict = self.parentApp.api_getters_dict[const.API_TYPES.LAUNCHES]()
        self.update_form()


    def h_decrement_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the previous values
        """
        self.launch_object_dict = self.parentApp.api_getters_dict[const.API_TYPES.LAUNCHES](False)
        self.update_form()

    def update_form(self):
        self.w_launch_selection.values = list(self.launch_object_dict.keys())