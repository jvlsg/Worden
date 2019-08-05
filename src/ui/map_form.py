import npyscreen, curses
import drawille
from src.ui.ui_utils import TextBox, HustonForm

class MapForm(HustonForm):
    def create(self, *args, **keywords):
        super(MapForm, self).create(*args, **keywords)

        self.w_map_selection = self.add(npyscreen.BoxTitle, name="",
            values=["WORLD", "ORBIT", "SYSTEM"],
            max_width=20,
            rely=self.PADDING_Y,
            relx=self.PADDING_X,
        )        

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
        
        self.map_canvas = drawille.Canvas()
        ##X,Y Coordinates that limit the frame size of the canvas
        #TODO
        self.map_canvas_frame_limits = (
            0,0,
            self.w_map_box.max_width*2,
            (self.w_map_box.max_height - self.w_map_box.rely)*4)

    def update_form(self):
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
        
        self.w_map_box.update(clear=True)            
        ##TODO Update positions/coordinates of trackable objects
        #self.update_obj_positions(...)
        self.redraw_canvas()
        

    def redraw_canvas(self):
        """
        Clears and redraws all trackable objects after they had their positions updated
        Sets the value of the map_box as the return of the Canvas.frame() function
        """
        self.map_canvas.clear()
        draw_map(self.map_canvas)

        ##TODO Redraw all other trackable objects
        #canvas.set(chart_height*2+chart_height,chart_height*2)   
        #Pense no canvas como uma dimensão paralela com coordenadas X,Y
        #O que de fato aparece na tela depende das coordenadas de COmeço e Fim
        #Do frame, i.e. da janelinha que vc está abrindo pra essa dimensão paralela    
        self.w_map_box.value=self.map_canvas.frame(
            self.map_canvas_frame_limits[0],
            self.map_canvas_frame_limits[1],
            self.map_canvas_frame_limits[2],
            self.map_canvas_frame_limits[3])



def draw_map(canvas):
    for line in enumerate(MAP):
        for column in enumerate(MAP[line[0]]):
            
            x = int(column[0] * 1.75)
            y = int(line[0] * 3.5)
            # x = int(column[0] * 1.1125)
            # y = int(line[0] * 3.25)        
            map_pos = MAP[line[0]][column[0]]
            if map_pos == " ":
                pass
            elif map_pos in ["|",")","("]:
                canvas.set(x,y)
                canvas.set(x,y+1)
                canvas.set(x,y+2)
                #c.set(x,y+3)
            elif map_pos == "/":
                #c.set(x+1,y)
                canvas.set(x+1,y+1)
                canvas.set(x,y+2)
                #c.set(x,y+3)            
            elif map_pos == "\\":
            # c.set(x,y)
                canvas.set(x,y+1)
                canvas.set(x+1,y+2)
            # c.set(x+1,y+3)            
            else:
                canvas.set(x,y)

MAP = [
"           , _-\','|~\~      ~/      ;-'_   _-'     ,;_;_,    ~~-     ",
"  /~~-\_/-'~'--' \~~| ',    ,'      /  / ~|-_\_/~/~      ~~--~~~~'--_ ",
"  /              ,/'-/~ '\ ,' _  , '|,'|~                   ._/-, /~  ",
"  ~/-'~\_,       '-,| '|. '   ~  ,\ /'~                /    /_  /~    ",
".-~      '|        '',\~|\       _\~     ,_  ,               /|       ",
"          '\        /'~          |_/~\\,-,~  \ '         ,_,/ |       ",
"           |       /            ._-~'\_ _~|              \ ) /        ",
"            \   __-\           '/      ~ |\  \_          /  ~         ",
"  .,         '\ |,  ~-_      - |          \\_' ~|  /\  \~ ,           ",
"               ~-_'  _;       '\           '-,   \,' /\/  |           ",
"                 '\_,~'\_       \_ _,       /'    '  |, /|'           ",
"                   /     \_       ~ |      /         \  ~'; -,_.      ",
"                   |       ~\        |    |  ,        '-_, ,; ~ ~\    ",
"                    \,      /        \    / /|            ,-, ,   -,  ",
"                     |    ,/          |  |' |/          ,-   ~ \   '. ",
"                    ,|   ,/           \ ,/              \       |     ",
"                    /    |             ~                 -~~-, /   _  ",
"                    |  ,-'                                    ~    /  ",
"                    / /'                                      ~       ",
"                    \|  ~                                            ",
"                      \\                                              ",
"                                          ._.--._ _..---.---------.__ ",
"          ,-----\--..?----_/ )      __,-\"                           \\",
"     -.._(                  `-----'                                   "
]
