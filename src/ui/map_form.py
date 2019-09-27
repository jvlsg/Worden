import npyscreen, curses
import drawille
import copy
from src.ui.ui_utils import TextBox, HustonForm
from PIL import Image
from collections import namedtuple
import logging

Area=namedtuple("Area",["min_x","min_y","max_x","max_y"])
MAP_IMAGE_FILEPATH = "src/ui/resources/mapimg.png"
MAP_IMAGE_THRESHOLD = 225

class MapForm(HustonForm):
    def create(self, *args, **keywords):
        super(MapForm, self).create(*args, **keywords)

        self.w_map_selection = self.add(npyscreen.BoxTitle, name="",
            values=["WORLD", "ORBIT", "SYSTEM"],
            max_width=20,
            rely=self.PADDING_Y,
            relx=self.PADDING_X,
            #check_value_change=True
        )
        #self.w_map_selection.when_value_edited = self.update_form

        
        self.w_map_box = self.add(TextBox,
            name="MAP",
            #max_width= self.USEABLE_X-self.w_map_selection.max_width - 2*self.PADDING_X, 
            max_width= self.USEABLE_X-self.w_map_selection.max_width-5, 
            max_height = self.USEABLE_Y-3,
            #Relx of the previous + width of the previous - Padding 
            relx = self.w_map_selection.relx + self.w_map_selection.width - 2*self.PADDING_X, 
            rely=self.PADDING_Y
            )       
        self.w_map_box.editable=False


        ##Pixel X,Y Coordinates that limit the size of the Map
        ## It is updated after setting
        self.map_pixel_limits = {
            "min_x":0,
            "min_y":0,
            "max_x":self.w_map_box.max_width*2,
            "max_y":(self.w_map_box.max_height - self.w_map_box.rely)*4
        }
        
        ##Canvas with Only the map. Each refresh just re-print
        ## this canvas instead of redrawing the entire map
        self.base_map_canvas = drawille.Canvas()
        self.draw_map_on_canvas(self.base_map_canvas,
            self.w_map_box.max_width,
            self.w_map_box.max_height)

        #Canvas where the objects will be tracked on
        self.map_canvas = drawille.Canvas()

    def update_form(self):
        """
        Clears the screen, redraws the map and 
        draw the tracked object if there is one
        Sets the value of the map_box as the return of the Canvas.frame() function
        """
        self.w_map_box.update(clear=True)
        self.map_canvas = copy.deepcopy(self.base_map_canvas)

        #WORLD MAP
        if (self.w_map_selection.get_value()==self.w_map_selection.values.index("WORLD")):
            self.draw_tracked_object()
            ##TODO Redraw all other trackable objects

        self.w_map_box.value=self.map_canvas.frame(
            self.map_pixel_limits["min_x"],
            self.map_pixel_limits["min_y"],
            self.map_pixel_limits["max_x"],
            self.map_pixel_limits["max_y"])


    def draw_tracked_object(self):
        """
        Converts latitude/longitude positions into Canvas positions
        Draws the current tracked object
        """
        footer_msg="NOW TRACKING: "
        if self.parentApp.tracked_object is None:
            footer_msg+="N/A"
        else:
            footer_msg+=str(self.parentApp.tracked_object.name)
            lat,lon = self.parentApp.tracked_object.track() 

            self.w_map_box.footer=footer_msg   
            point = convert_gps_coord_to_canvas_coord(
                lat,lon,
                self.map_pixel_limits)
            self.map_canvas.set(point[0],point[1])

            h_line = drawille.line(self.map_pixel_limits["min_x"],point[1],self.map_pixel_limits["max_x"],point[1])
            v_line = drawille.line(point[0],self.map_pixel_limits["min_y"],point[0],self.map_pixel_limits["max_y"])
            for i in v_line:
                self.map_canvas.set(i[0],i[1])
            for i in h_line:
                self.map_canvas.set(i[0],i[1])


    def draw_map_on_canvas(self,canvas,widget_max_width,widget_max_height):
        """
        Draw a worldmap onto a Canvas
    
        Args:
            canvas: The canvas to draw
            widget_max_width: Width in columns of the widget that will print the canvas
            widget_max_height: Height in lines of the widget that will print the canvas
        """
    
        #Determine if the size of the image is greater than the size to print, if so, scale it down
        f = open(MAP_IMAGE_FILEPATH,'rb') #Open in binary mode
        i = Image.open(f).convert('L')
        image_width, image_height = i.size
    
        #Converts from columns to 'drawille pixels'
        widget_max_width = self.map_pixel_limits["max_x"]
        widget_max_height = self.map_pixel_limits["max_y"]
    
        w_ratio = 1    
        if widget_max_width < image_width:
            w_ratio = widget_max_width / float(image_width)
    
        h_ratio = 1
        if widget_max_height < image_width:
            h_ratio = widget_max_height / float(image_height)
        
        ratio = 0.8*min([w_ratio,h_ratio])
        image_width = int(image_width * ratio)
        image_height = int(image_height * ratio)
        i = i.resize((image_width, image_height), Image.ANTIALIAS)
        #Update limits
        self.map_pixel_limits["max_y"] = image_height
        self.map_pixel_limits["max_x"] = image_width
                
        #logging.debug("Map to Canvas: Ratio {}\n\tWidget Size(px): W {} x H {}\n\tImg Size (px): W {} x H {}".format(ratio,widget_max_width, widget_max_height,image_width,image_height)) 
        #logging.debug("Map Pixel Limits: {}".format(self.map_pixel_limits))
        try:
            i_converted = i.tobytes()
        except AttributeError:
            #i_converted = i.tostring()
            raise
    
        x = y = 0
        for pix in i_converted:
            if pix < MAP_IMAGE_THRESHOLD:
                canvas.set(x, y)
            x += 1
            if x >= image_width:
                y += 1
                x = 0

def convert_gps_coord_to_canvas_coord(latitude,longitude,map_pixel_limits):
    """
    Converts Latitude/Longitude to coordinates

    args:
        latitude: number between -90 and 90
        longitude: number between -180 and 180 
        map_pixel_limits: 
    returns:
    """
    if int(latitude) not in range(-90,90):
        raise IndexError
    if int(longitude) not in range(-180,180):
        raise IndexError

    #The canvas Y Axis is positive downwards, therefore we negate the latitude for %
    latitude_in_perc = abs((-latitude + 90)/180)
    longitude_in_perc = abs((longitude + 180)/360)

    x_range = map_pixel_limits["max_x"] - map_pixel_limits["min_x"]
    y_range = map_pixel_limits["min_y"] - map_pixel_limits["max_y"]
    
    x_coord = int(abs( map_pixel_limits["min_x"] + longitude_in_perc * x_range))
    y_coord = int(abs( map_pixel_limits["min_y"] + latitude_in_perc * y_range))

    #logging.debug("GPS longitude {},latitude {} to Pixel {},{}".format(longitude,latitude,x_coord,y_coord))
    return (x_coord,y_coord)



"""
Drawile "PIXEL"
dots:
,___,
|1 4|
|2 5|
|3 6|
|7 8|
`````
"""