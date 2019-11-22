import npyscreen, curses
import logging
import src.const as const

class TextBox(npyscreen.BoxTitle):
    # MultiLineEdit now will be surrounded by boxing
    _contained_widget = npyscreen.MultiLineEdit

class WordenForm(npyscreen.FormBaseNewWithMenus):
    """
    Generic npyscreen Form used by other Forms containing Standard Handlers
    """

    def create(self, *args, **keywords):
        super(WordenForm, self).create(*args, **keywords)
        
        self.USEABLE_Y, self.USEABLE_X = self.useable_space()
        self.PADDING_X = 1
        self.PADDING_Y = 1
        #None or one of the values described in API_TYPES Enum
        self.api_type = None
        self.menu = self.add_menu(name="Main Menu")
        self.menu.addItem(text="MAP",onSelect=self.h_change_form,arguments=["MAIN"])
        self.menu.addItem(text="LAUNCHES",onSelect=self.h_change_form,arguments=[const.API_TYPES.LAUNCHES])
        self.menu.addItem(text="ASTRONAUTS",onSelect=self.h_change_form,arguments=[const.API_TYPES.ASTRONAUTS])
        self.menu.addItem(text="EXIT",onSelect=self.h_close_application)

        new_handlers={
            "^R" : self.h_update,
            "^T" : self.h_track_object,
            ">" : self.h_increment_offset,
            "<" : self.h_decrement_offset,
            }
        self.add_handlers(new_handlers)
    
    def h_close_application(self):
        self.parentApp.setNextForm(None)
        self.editing = False
        logging.debug("Closing Application")
        self.parentApp.switchFormNow()

    def h_change_form(self,*args,**keywords):
        """
        Changes the current active form of the App
        """
        if args[0] not in list(self.parentApp._Forms.keys()):
            err_str = "Invalid Form name: {}".format(args[0])
            logging.error(err_str)
            raise KeyError(err_str)
        logging.debug("Changing Form to {}".format(args[0]))
        self.parentApp.change_form_to(args[0])

    
    def h_increment_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the next values
        """
        pass

    def h_decrement_offset(self, *args, **keywords):
        """
        Method used by forms that manipulate API data, to fetch the previous values
        """
        pass

    def h_track_object(self, *args,**keywords):
        """
        Wrapper Used by Keyboard Handler to invoke the Form's Track function
        """
        self.track_object()

    def track_object(self):
        """
        Function that Track a currently selected.
        """
        pass

    def h_update(self,_input):
        """
        Wrapper Used by Keyboard Handler to invoke the Form's Update function
        """
        self.update_form()

    def update_form(self):
        """
        Function that updates form.
        If necessary, it should contain the functions for a basic Update/Draw loop
        """
        pass