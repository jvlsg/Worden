import npyscreen, curses
import drawille
from src.ui.ui_utils import TextBox

class MapForm(npyscreen.FormBaseNew):
    def create(self, *args, **keywords):
        super(MapForm, self).create(*args, **keywords)
        
        USEABLE_Y, USEABLE_X = self.useable_space()
        PADDING_X = 1
        PADDING_Y = 1


        self.w_map_selection = self.add(npyscreen.BoxTitle, name="",
            values=["WORLD", "ORBIT", "SYSTEM"],
            max_width=20,
            rely=PADDING_Y,
            relx=PADDING_X,
        )        

        self.map_canvas = drawille.Canvas()
        self.w_map_box = self.add(TextBox,
            name="MAP",
            max_width= USEABLE_X-self.w_map_selection.max_width - 2*PADDING_X, 
            max_height = USEABLE_Y-3,
            #Relx of the previous + width of the previous - Padding 
            relx = self.w_map_selection.relx + self.w_map_selection.width - 2*PADDING_X, 
            rely=PADDING_Y
            )       
        self.w_map_box.editable=False

        new_handlers={
            "^R" : self.h_update,
            curses.KEY_F2 : self.h_change_form
            }
        self.add_handlers(new_handlers)

    def h_change_form(self,_input):
        to=""
        if(_input == curses.KEY_F1):
            to="MAIN"
        elif(_input == curses.KEY_F2):
            to="SECONDARY"
        else:
            to="MAIN" 
        self.parentApp.change_form(to)

    def h_update(self,_input):
        self.update()


    def update(self):
        self.w_map_box.update(clear=True)
        self.w_map_box.value=(self.draw_chart(self.map_canvas,self.w_map_box,self.dot_pos))
        self.dot_pos=(self.dot_pos[0]+1,self.dot_pos[1]+1)
        self.w_map_box.footer="NOW TRACKING: EXAMPLE | Width {} Height {}\tDot X:{} Y:{}".format(
            self.w_map_box.width,self.w_map_box.height,self.dot_pos[0],self.dot_pos[1])
        
    def draw_chart(self,canvas,chart,pos):
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
        canvas.clear()
        map.draw_map(canvas)
        window_max_x,window_max_y = self.useable_space()
        max_x = chart.max_width*2 - window_max_x - 2
        max_y = (chart.max_height - chart.rely)*4
        
        canvas.set(pos[0],pos[1])

        chart.name="Max Pix X: {} Y: {}".format(max_x,max_y)

        #canvas.set(chart_height*2+chart_height,chart_height*2)   

        #Pense no canvas como uma dimensão paralela com coordenadas X,Y
        #O que de fato aparece na tela depende das coordenadas de COmeço e Fim
        #Do frame, i.e. da janelinha que vc está abrindo pra essa dimensão paralela    
        return canvas.frame(0,0,max_x,max_y)
