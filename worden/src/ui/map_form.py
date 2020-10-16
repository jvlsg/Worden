import npyscreen, curses
import drawille
import copy
from worden.src.ui.ui_utils import TextBox, WordenForm, draw_image_on_canvas
from PIL import Image
from collections import namedtuple
import logging
import worden.const as const

Area=namedtuple("Area",["min_x","min_y","max_x","max_y"])

class MapForm(WordenForm):
    def create(self, *args, **keywords):
        super(MapForm, self).create(*args, **keywords)

        self.w_map_selection = self.add(npyscreen.BoxTitle, name="",
            values=["WORLD"],
            #values=["WORLD", "ORBIT", "SYSTEM"],
            max_width=20,
            rely=self.PADDING_Y,
            relx=self.PADDING_X,
            #check_value_change=True
        )
        self.w_map_selection.value = 0
        
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
        draw_image_on_canvas(open(const.MAP_IMAGE_FILEPATH,'rb'),
            const.MAP_IMAGE_THRESHOLD,
            False,
            self.base_map_canvas,
            self.map_pixel_limits)
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
        footer_msg="TRACKING:"
        if self.parentApp.tracked_object is None:
            footer_msg+=" -"
            self.w_map_box.footer=footer_msg
            return
        
        coords = self.parentApp.tracked_object.track_global_coordinates()
        if coords == None:
            footer_msg+="\"{}\" COORDS:(N/A)".format(str(self.parentApp.tracked_object.name))

        else:
            lat,lon = coords
            coord_msg="{},{}".format(round(lat,2),round(lon,2))
            footer_msg+="\"{}\" COORDS:({})".format(str(self.parentApp.tracked_object.name),coord_msg)
            point = convert_gps_coord_to_canvas_coord(
                lat,lon,
                self.map_pixel_limits)
            self.map_canvas.set(point[0],point[1])
            #self.map_canvas.set_text(point[0],point[1],coord_msg)
            h_line = drawille.line(self.map_pixel_limits["min_x"],point[1],self.map_pixel_limits["max_x"],point[1])
            v_line = drawille.line(point[0],self.map_pixel_limits["min_y"],point[0],self.map_pixel_limits["max_y"])
            for i in v_line:
                self.map_canvas.set(i[0],i[1])
            for i in h_line:
                self.map_canvas.set(i[0],i[1])

        self.w_map_box.footer=footer_msg   


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