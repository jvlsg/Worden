import npyscreen, curses
import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG)

class TextBox(npyscreen.BoxTitle):
    # MultiLineEdit now will be surrounded by boxing
    _contained_widget = npyscreen.MultiLineEdit

class HustonForm(npyscreen.FormBaseNew):
    """
    Generic npyscreen Form used by other Huston Forms containing Standard Handlers
    """

    def create(self, *args, **keywords):
        super(HustonForm, self).create(*args, **keywords)
        
        self.USEABLE_Y, self.USEABLE_X = self.useable_space()
        self.PADDING_X = 1
        self.PADDING_Y = 1

        new_handlers={
            "^R" : self.h_update,
            curses.KEY_F1 : self.h_change_form,
            curses.KEY_F2 : self.h_change_form,
            curses.KEY_F3 : self.h_change_form,
            curses.KEY_F4 : self.h_change_form,
            curses.KEY_F5 : self.h_change_form,
            }
        self.add_handlers(new_handlers)


    def h_change_form(self,_input):
        """
        Handler function to change the App's current form 
        """

        #Input between F1 and F12
        if _input < curses.KEY_F1 or _input > curses.KEY_F12:
            return
        input_offset = _input - curses.KEY_F1
        
        logging.debug("h_change_form input: {}\ninput_offset: {}".format(_input,input_offset))        
        valid_forms = list(self.parentApp._Forms.keys())
        next_form = ""

        try:
            next_form = valid_forms[input_offset]
        except IndexError:
            next_form = "MAIN"
        finally:
            logging.debug("Next Form:{} Valid Forms {}".format(next_form,str(valid_forms)))
            self.parentApp.change_form_to(next_form)

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