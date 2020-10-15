import npyscreen, curses
import logging
import src.const as const
from PIL import Image

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
        for api_type in const.API_TYPES:
            self.menu.addItem(text=api_type.value,onSelect=self.h_change_form,arguments=[api_type])
        self.menu.addItem(text="EXIT",onSelect=self.h_close_application)

        new_handlers={
            const.CONTROLS["update"] : self.h_update,
            const.CONTROLS["track"] : self.h_track_object,
            const.CONTROLS["increment_offset"] : self.h_increment_offset,
            const.CONTROLS["decrement_offset"] : self.h_decrement_offset,
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

def draw_image_on_canvas(image_descriptor=None,color_threshold=0,invert_threshold=False,canvas=None,pixel_limits=None):
    """
    Draws an image onto a Canvas

    Args:
        image_descriptor: open in binary mode e.g. open(MAP_IMAGE_FILEPATH,'rb') requests.get('...',stream=True)
        color_threshold: int (0-255) to paint (or not) a pixel in drawille
        invert_threshold: if set to True, the threshold test will be: paint when pixel color > threshold 
        canvas: The canvas to draw
        pixel_limits: a dict of X,Y Coordinates that limit the size of the image, used by canvas.frame(...)
            If the image size is greater than the limits, the image is resized maintaining the ratio and
            the pixel limits are updated 
            pixel_limits = {"min_x":0,"min_y":0,"max_x":128,"max_y":128}

    Returns: None. 
    """

    #Determine if the size of the image is greater than the size to print, if so, scale it down
    i = Image.open(image_descriptor).convert(mode='L')
    image_width, image_height = i.size   

    w_ratio = 1    
    if  pixel_limits["max_x"] < image_width:
        w_ratio =  pixel_limits["max_x"] / float(image_width)

    h_ratio = 1
    if pixel_limits["max_y"] < image_width:
        h_ratio = pixel_limits["max_y"] / float(image_height)
    
    ratio = 0.8*min([w_ratio,h_ratio])
    image_width = int(image_width * ratio)
    image_height = int(image_height * ratio)
    i = i.resize((image_width, image_height), Image.ANTIALIAS)
    #Update limits
    pixel_limits["max_y"] = image_height
    pixel_limits["max_x"] = image_width
            
    try:
        i_converted = i.tobytes()
    except AttributeError:
        raise
    
    if invert_threshold:
        threshold_test = lambda pix_color,color_threshold: pix_color > color_threshold
    else:
        threshold_test = lambda pix_color,color_threshold: pix_color < color_threshold

    x = y = 0
    for pix in i_converted:
        if threshold_test(pix,color_threshold):
            canvas.set(x, y)
        x += 1
        if x >= image_width:
            y += 1
            x = 0