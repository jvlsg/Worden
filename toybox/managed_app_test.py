#!/usr/bin/env python
import npyscreen, curses
import random, math
import drawille

MAP = """
            ,_   .  ._. _.  .
           , _-\','|~\~      ~/      ;-'_   _-'     ,;_;_,    ~~-
  /~~-\_/-'~'--' \~~| ',    ,'      /  / ~|-_\_/~/~      ~~--~~~~'--_
  /              ,/'-/~ '\ ,' _  , '|,'|~                   ._/-, /~
  ~/-'~\_,       '-,| '|. '   ~  ,\ /'~                /    /_  /~
.-~      '|        '',\~|\       _\~     ,_  ,               /|
          '\        /'~          |_/~\\,-,~  \ "         ,_,/ |
           |       /            ._-~'\_ _~|              \ ) /
            \   __-\           '/      ~ |\  \_          /  ~
  .,         '\ |,  ~-_      - |          \\_' ~|  /\  \~ ,
               ~-_'  _;       '\           '-,   \,' /\/  |
                 '\_,~'\_       \_ _,       /'    '  |, /|'
                   /     \_       ~ |      /         \  ~'; -,_.
                   |       ~\        |    |  ,        '-_, ,; ~ ~\
                    \,      /        \    / /|            ,-, ,   -,
                     |    ,/          |  |' |/          ,-   ~ \   '.
                    ,|   ,/           \ ,/              \       |
                    /    |             ~                 -~~-, /   _
                    |  ,-'                                    ~    /
                    / ,'                                      ~
                    ',|  ~
                      ~'
"""

def circle(canvas,x0=0,y0=0,radius=0):
    for g in range(0,360,36):
        t = math.radians(g)
        x = x0 + math.cos(t) * radius
        y = y0 + math.sin(t) * radius
        canvas.set(x,y)

    #npyscreen.disableColor()
class InputBox(npyscreen.BoxTitle):
    # MultiLineEdit now will be surrounded by boxing
    _contained_widget = npyscreen.MultiLineEdit

class SecForm(npyscreen.FormBaseNew):
    def create(self):
        self.add(npyscreen.TitleFixedText, name = "Fixed Text:" , value="This is fixed text")
        self.add(npyscreen.TitleText, name = "Text:", )
        self.add(npyscreen.TitlePassword, name = "Password:")
        self.add(npyscreen.TitleFilename, name = "Filename:")
        self.add(npyscreen.TitleDateCombo, name = "Date:")
        self.add(npyscreen.Checkbox, name = "A Checkbox")
        self.add(npyscreen.TitleSlider, out_of=12, name = "Slider")
        self.add(npyscreen.MultiLineEdit, 
            value = """try typing here! Mutiline text, press ^R to reformat.\nPress ^X for automatically created list of menus""", 
            max_height=5, rely=9)
        self.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
                values = ["Option1","Option2","Option3"], scroll_exit=True, width=30)
        self.add(npyscreen.MultiSelect, max_height=4, value = [1,], 
                values = ["Option1","Option2","Option3"], scroll_exit=True, width=20)

        self.add(npyscreen.MiniButton, name = "Button",)
        
        #gd = F.add(npyscreen.SimpleGrid, relx = 42, rely=15, width=20)
        gd = self.add(npyscreen.GridColTitles, relx = 42, rely=15, width=20, col_titles = ['1','2','3','4'])
        gd.values = []
        for x in range(36):
            row = []
            for y in range(x, x+36):
                row.append(y)
            gd.values.append(row)


        new_handlers={
            curses.KEY_F1 : self.h_change_form
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


class MainForm(npyscreen.FormBaseNew):
    def create(self, *args, **keywords):
        super(MainForm, self).create(*args, **keywords)
        self.form_canvas = drawille.Canvas()
        y, x = self.useable_space()
        self.dot_pos=(10,10)

        obj = self.add(npyscreen.BoxTitle, name="Window Useable Space",
            values=["X {}".format(x), "Y {}".format(y)],
            max_width=20, 
            max_height=y-5,
            rely=2
            )        

        self.t = self.add(InputBox,
            name="CHART",
            max_width= 40, 
            max_height = y-5,
            relx = obj.relx + obj.width + 1, 
            rely=2
            )       
        self.t.value=MAP 
        self.t.editable=False
        self.t.footer="Width {} Height {}\tDot X:{} Y:{}".format(
            self.t.width,self.t.height,self.dot_pos[0],self.dot_pos[1])

        self.t2 = self.add(InputBox,
            name="CHART",
            max_width= x-(self.t.max_width+self.t.relx+obj.max_width+obj.relx) , 
            max_height = y-5,
            relx= self.t.width + self.t.relx + 1, 
            rely=2
        )        
        
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
        self.t.update(clear=True)
        self.t.value=(self.draw_chart(self.form_canvas,self.t,self.dot_pos))
        self.dot_pos=(self.dot_pos[0]+1,self.dot_pos[1]+1)
        self.t.footer="Width {} Height {}\tDot X:{} Y:{}".format(
            self.t.width,self.t.height,self.dot_pos[0],self.dot_pos[1])
        
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
        
        window_max_x,window_max_y = self.useable_space()
        max_x = chart.max_width*2 - window_max_x - 2
        max_y = (chart.max_height - chart.rely)*4
        
        canvas.set(pos[0],pos[1])

        chart.name="Max Pix X: {} Y: {}".format(max_x,max_y)

        #canvas.set(chart_height*2+chart_height,chart_height*2)   

        #Pense no canvas como uma dimensão paralela com coordenadas X,Y
        #O que de fato aparece na tela depende das coordenadas de COmeço e Fim
        #Do frame, i.e. da janelinha que vc está abrindo pra essa dimensão paralela    
        circle(canvas,pos[0],pos[1],5)

        return canvas.frame(0,0,max_x,max_y)


class TestApp(npyscreen.NPSAppManaged):
    def while_waiting(self):
        #UPDATE THE CURRENT FORM / FETCH API 
        self.w1.update()
    
    def onStart(self):
        #THIS NEEDS TO BE BEFORE REGISTERING THE FORM 
        self.keypress_timeout_default = 10

        self.w1 = MainForm(parentApp=self, name = "ACTIVE ASSETS")
        self.w2 = SecForm(parentApp=self, name="LAUNCHES")

        self.registerForm("MAIN",self.w1)
        self.registerForm("SECONDARY",self.w2)

    # def onCleanExit(self):
    #     npyscreen.notify_wait("Goodbye!")
    
    def change_form(self, name):
        # Switch forms.  NB. Do *not* call the .edit() method directly (which 
        # would lead to a memory leak and ultimately a recursion error).
        # Instead, use the method .switchForm to change forms.
        self.switchForm(name)
        
        # By default the application keeps track of every form visited.
        # There's no harm in this, but we don't need it so:        
        self.resetHistory()
    

if __name__ == "__main__":
    App = TestApp()
    App.run()
