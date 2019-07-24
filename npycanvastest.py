#!/usr/bin/env python
import npyscreen
import random, math
import drawille

#npyscreen.disableColor()
class InputBox(npyscreen.BoxTitle):
    # MultiLineEdit now will be surrounded by boxing
    _contained_widget = npyscreen.MultiLineEdit

    
class MainForm(npyscreen.FormBaseNew):
    def create(self, *args, **keywords):
        super(MainForm, self).create(*args, **keywords)

        y, x = self.useable_space()
        self.dot_pos=(0,0)

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

        # fn = window.add(npyscreen.TitleFilename, name = "Filename:")
        # dt = window.add(npyscreen.TitleDateCombo, name = "Date:")
        # s = window.add(npyscreen.TitleSlider, out_of=12, name = "Slider", color='DANGER')
        #ml= window.add(npyscreen.MultiLineEdit, 
            # value = """try typing here!\nMutiline text, press ^R to reformat.\n""", 
            # max_height=5, rely=0)
        # ms= window.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One", 
        #         values = ["Option1","Option2","Option3"], scroll_exit=True)

    def update(self):
        self.t.value=(self.draw_chart(self.t,self.dot_pos))
        self.t.update(clear=True)

        self.dot_pos=(self.dot_pos[0]+1,self.dot_pos[1]+1)
        self.t.footer="Width {} Height {}\tDot X:{} Y:{}".format(
            self.t.width,self.t.height,self.dot_pos[0],self.dot_pos[1])
        
    def draw_chart(self,chart,pos):
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

        window_max_x,window_max_y = self.useable_space()
        
        max_x = chart.width*2 - window_max_x - 2
        max_y = (chart.height - chart.rely)*4

        canvas = drawille.Canvas()
        
        #for x in range(max_x):
        #    canvas.set(x, math.sin(math.radians(x)) * 10)
        
        # for x in range(max_x):
        #     canvas.set(x,0)

        # for y in range(max_y):
        #     canvas.set(0,y)

        canvas.set(pos[0],pos[1])

        chart.name="Max Pix X: {} Y: {}".format(max_x,max_y)

        #canvas.set(chart_height*2+chart_height,chart_height*2)   

        #Pense no canvas como uma dimensão paralela com coordenadas X,Y
        #O que de fato aparece na tela depende das coordenadas de COmeço e Fim
        #Do frame, i.e. da janelinha que vc está abrindo pra essa dimensão paralela    
        return canvas.frame(0,0,max_x,max_y)
        

class TestApp(npyscreen.NPSApp):
    def while_waiting(self):
        self.window.update()
        
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        self.keypress_timeout_default = 1
        
        self.window = MainForm(parentApp=self, name = "Welcome to Npyscreen",)
        
        # This lets the user play with the Form.
        self.window.edit()


if __name__ == "__main__":
    App = TestApp()
    App.run()
