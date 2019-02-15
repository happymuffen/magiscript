from kivy.app import App
from kivy.uix.widget import Widget

class ItemIcon(Widget):
	pass

class MenuCircle(Widget):
	pass

class MagScreen(Widget):
	pass

class MagApp(App):
	def build(self):
		return MagScreen()
	
if __name__ == '__main__':
    MagApp().run()
