from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle
import math, random

c=[0.0,0.0]


def car_to_pol(car):
	global c
	pol= [sqrt((car[0]-c[0])**2+(car[1]-c[1])**2), atan((car[1]-c[1])/car[0]-c[0])]
	return pol

def pol_to_car(pol):
	global c
	car= [pol[0]*cos(pol[1]), pol[0]*sin(pol1)]
	return car
	
class Conector(Widget):
	#needs to be able to path around items it isn't connected to
	#needs to handle overlap
	pass

class ItemIcon(Widget):
	#needs to avoid being placed on top of anything important
	#needs to open selection window
	#needs to differentiate between movement comand and selection comand
	#^ differentiate by time for click
	pass
	
class SelectionWindow(Widget):
	#needs to allow input of variables
	#needs to handle click offs
	pass
	
class MenuIcon(Widget):
	#needs to make moving icon
	pass

class MenuCircle(Widget):
	def __init__(self, **kwargs):
		super(MenuCircle, self).__init__(**kwargs)
		global c
		self.pos=[c[0]-50,c[1]-50]
		local_c=c
		options=["start_node", "time", "variables","flow control","network","I/O","Sound/Notifications", "Interface"]
		with self.canvas:
			Color(.3,.3,.3)
			Line(circle=(c[0],c[1],100),width=5)
		
class MagScreen(FloatLayout):
	def __init__(self, **kwargs):
		super(MagScreen, self).__init__(**kwargs)
		global c
		c=Window.center
		self.size=Window.size
		with self.canvas:
			Rectangle(pos=self.pos,size=self.size)
		mc=MenuCircle()
		self.add_widget(mc)

class Magiscript(App):
	def build(self):
		self.layout=MagScreen()
		
		return self.layout
		
if __name__ == '__main__':
    Magiscript().run()
    
# ~ class OutStream(Label):
	# ~ def __init__(self, **kwargs):
		# ~ super(OutStream, self).__init__(**kwargs)
		# ~ self.text="test"
		# ~ self.color=[.3,.3,.3]
	# ~ def update(self,s):
		# ~ self.text=str(s)
	# ~ def on_touch_down(self,touch):
		# ~ self.update(touch)
