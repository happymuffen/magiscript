from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, SmoothLine, Rectangle
from kivy.graphics.instructions import Instruction, InstructionGroup
import math, random, datetime
from kivy.config import Config

c=Window.center
ringi=110
inuse=[]
buf=(100+ringi)*math.pi/6

#add drawpercentage() to all visible classes for animating loading saves

def get_dis(c1,c2):
	#returns the distance between two points
	return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
	
def car_to_pol(car,c=c):
	#gets polar coords relative to center from cartisian [r,t]
	dx=car[0]-c[0]
	#can't divide by 0
	if dx==0:
		dx=.0000000000000000001
	#atan(x) only outputs +/-180
	b=0
	if dx<0:
		b=180
	pol= [get_dis(c,car), math.degrees(math.atan((car[1]-c[1])/dx))+b]
	if pol[1]<0:
		pol[1]+=360
	return pol

def pol_to_car(pol,c=c):
	#gets cartisian coords to polar from center [x,y]
	car= [pol[0]*math.cos(math.radians(pol[1]))+c[0], pol[0]*math.sin(math.radians(pol[1]))+c[1]]
	return car
		
def findcircleintersections(cir0,cir1):
	#finds 0, 1, or 2 intersections between any 2 cirlces in the form of [cx,cy,r]
	d=get_dis([cir0[0],cir0[1]],[cir1[0],cir1[1]])
	if cir0[2]+cir1[2] < d or abs(cir0[2]-cir1[2]) > d or d==0: return [[]]
	ux=(cir0[0]-cir1[0])/d
	uy=(cir0[1]-cir1[1])/d
	a=(cir0[2]**2-(cir1[2]**2)+(d**2))/d/-2
	if a==cir0[2]:return [[a*ux+cir0[0],a*uy+cir0[1]]]
	h=math.sqrt(cir0[2]**2-a**2)
	out= [[a*ux-h*uy+cir0[0],a*uy+h*ux+cir0[1]],[a*ux+h*uy+cir0[0],a*uy-h*ux+cir0[1]]]
	return out

def listofshapes(r):
	
	global inuse
	global buf
	l=[]
	for each in inuse:
		l.append([each[0],each[1],r+buf+each[2]])
	return l
					
def makepoint(coords,canvas):
	canvas.add(Color(1,0,0))
	canvas.add(SmoothLine(circle=(coords[0],coords[1],2),width=3))
	
	
def intersects(cir0,cir1):
	#tests for intersections in two circles quickly
	d=get_dis([cir0[0],cir0[1]],[cir1[0],cir1[1]])
	if cir0[2]+cir1[2] < d:return 0#seperate circles
	if cir1[2]-cir0[2] > d: return -1#the first is inside the second
	if cir0[2]-cir1[2] > d: return -2#the second is inside the first
	if cir0[2]-cir1[2] ==d: return -3#intersection at 1 point(or same circle)
	return 1 #there is an intersection
	
class SelectionWindow(Widget):
	#needs to allow input of variables
	#needs to handle click offs
	pass
	
class Conector(Widget):
	pass

class MovingConector(Widget):
	#needs to be able to path around items it isn't connected to
	#needs to handle overlap
	def __init__(self, **kwargs):
		super(MovingConector,self).__init__(**kwargs)
		
	def init(self,c1,r1):
		self.c1,self.r1=c1,r1
		self.canvas.opacity=.2		
		
	def draw(self,path):
		self.canvas.clear()
		for group in [path]:
			self.canvas.add(group)	
	
	def on_touch_move(self,touch):
		l=self.limitpos(touch.pos)
		path=self.makepath(l)
		self.draw(path)
	
	def on_touch_up(self,touch):
		
		self.parent.remove_widget(self)
	
	
	
	def limitpos(self,coords):
		#should find snap location for coords
		return coords
	
	def makepath(self,coords):
		#returns InstructionGroup containing all relevent things to draw.
		todraw=InstructionGroup()
		todraw.add(SmoothLine(points=[self.c1[0],self.c1[1],coords[0],coords[1]],cap='round', joint='round', width=3))
		return todraw
			

class ItemIcon(Widget):
	#needs to avoid being placed on top of anything important
	#needs to open selection window
	#needs to differentiate between movement comand and selection comand
	#^ differentiate by time for click
	def __init__(self, **kwargs):
		super(ItemIcon,self).__init__(**kwargs)
		if kwargs is not None:
			for key, value in kwargs.items():
				if(key=='pos'): self.local_c=value
		self.r=0
		self.click=False
		self.time=-1
		
	def makeicon(self,r):
		self.r=r
		global inuse
		inuse.append([self.local_c[0],self.local_c[1],self.r])
		
		self.canvas.clear()
		self.icon=InstructionGroup()
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(Color(1,1,1))
		self.icon.add(Ellipse(size=(2*self.r,2*self.r),pos=(self.local_c[0]-self.r,self.local_c[1]-self.r)))
		self.icon.add(SmoothLine(circle=(self.local_c[0],self.local_c[1],self.r+4),width=3))
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(SmoothLine(circle=(self.local_c[0],self.local_c[1],self.r),width=3))
		for group in [self.icon]:
			self.canvas.add(group)	
	
	def now(self):
		now=datetime.datetime.now()
		return int(now.strftime("%M"))*60+int(now.strftime("%s"))
	
	def on_touch_down(self,touch):
		if get_dis(self.local_c,touch.pos) < self.r:
			self.click=True
			self.time=self.now()
			#test for click&drag
			#test for connecting
	
	def on_touch_move(self,touch):
		if self.click:
			if self.time<0:
				global inuse
				try:
					inuse.remove([self.local_c[0],self.local_c[1],self.r])
				except ValueError:
					pass
				
				a=MovingIcon(pos=touch.pos)
				a.init(self.r)
				self.parent.add_widget(a)#adds moving icon to screen
				self.parent.remove_widget(self)
			else:
				time=self.now()
				if self.time>time:
					time+=3600
				if time-self.time>0:
					a=MovingConector()
					a.init(self.local_c,self.r)
					self.parent.add_widget(a)
					self.click=False
				self.time=-1

class MovingIcon(Widget):
	#folows cursor while held
	#spawns ItemIcon if released at valid location
	#despawns when released
	def __init__(self, **kwargs):
		super(MovingIcon,self).__init__(**kwargs)
		global c
		self.c=c
		self.local_c=[0,0]
		self.pointslist=[]
		if kwargs is not None:
			for key, value in kwargs.items():
				if(key=='pos'): self.local_c=value
	
	def makepoint(self,coords):
		self.pointslist.append(coords)
		
	def init(self,r):
		self.l=listofshapes(r)
		self.r=r
		self.updateloc(self.local_c)
	
	def updateloc(self, coords):
		self.local_c=coords
		self.canvas.clear()
		self.icon=InstructionGroup()
		self.canvas.opacity=.2		
		self.icon.add(Color(1,1,1))
		self.icon.add(Ellipse(size=(2*self.r,2*self.r),pos=(self.local_c[0]-self.r,self.local_c[1]-self.r)))
		self.icon.add(SmoothLine(circle=(self.local_c[0],self.local_c[1],self.r+4),width=3))
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(SmoothLine(circle=(self.local_c[0],self.local_c[1],self.r),width=3))
		for group in [self.icon]:
			self.canvas.add(group)
		
		#handles makepoint
		if len(self.pointslist)>0:
			self.canvas.add(Color(.1,.1,.1))
			for each in self.pointslist:
				self.canvas.add(SmoothLine(circle=(each[0],each[1],5),width=1))
			self.pointslist=[]
			
	def on_touch_move(self, touch):
		l=self.limitpos(touch.pos)
		self.updateloc(l)
	
	def limitpos(self,coords):
		self.makepoint(coords)
		#limits possible locations
		
		#if a valid ring is not near just return coords
		#find closest location on that ring to coords
		#if that spot is free return it
		#find the intersections between the ring and what is occupying it
		#if neither is near coords return coords
		#check if the nearest intersection is free
			#if it is return it
			#if it isn't find whats blocking it and add it's farther intersection to the list
		#jmp to checking if intersections are close enough	
		
		#snap if within 35
		
		#sort function for finding the shortest distance between coords
		def sort_by_d(arr,coords):
			if arr==[[]]: return []
			def itersort_d(lh):
				l=lh[0]
				h=lh[1]
				p=l
				ldist=get_dis(arr[l],coords)
				for i in range(l+1,h):
					if get_dis(arr[i],coords)<ldist:
						p+=1
						arr[p],arr[i] = arr[i],arr[p]
				arr[p], arr[l]= arr[l],arr[p]
				return [l,p,h]
			pars=[[0,len(arr)]]
			while len(pars)>0:
				newpars=[]
				for each in pars:
					o=itersort_d(each)
					l,p,h=o[0],o[1],o[2]
					if not p-l<=1:newpars.append([l,p])
					if not h-p<=1:newpars.append([p+1,h])
				pars=newpars
			return arr
		
		ipol=car_to_pol(coords)
		pr=self.parent.r
		pc=self.parent.local_c
		max_d=40
		global ringi
		ringn=(ipol[0]-pr+(ringi/2))//ringi
		newr=pr+(ringn*ringi)
		if abs(newr-ipol[0])>max_d: return coords
		if newr<=pr:return coords
		newcoords=pol_to_car([newr,ipol[1]])
		cir=self.isbad(newcoords)
		if cir==[]: return newcoords
		interlist=findcircleintersections(cir,[pc[0],pc[1],newr])
		interlist=sort_by_d(interlist,coords)
		tmp=[]
		counter=0
		while counter<5:
			for each in interlist:
				b=False
				if get_dis(each,coords)<max_d:
					test=self.isbad(each)
					if test==[]:return each
					tl=findcircleintersections(test,[pc[0],pc[1],newr])
					for t in tl:
						for i in interlist:
							if t==i: b=True
						if b:break
						tmp.append(t)
					#update tmp
			if tmp==[]: break
			interlist=sort_by_d(tmp,coords)
			tmp=[]		
			counter+=1
	
		return coords
	
	def on_touch_up(self,touch):
		if self.isbad(self.local_c)==[]:
			a=ItemIcon(pos=self.local_c)
			a.makeicon(self.r)
			self.parent.add_widget(a)
		self.parent.remove_widget(self)
	
	def isbad(self, coords):
		global buf
		r=get_dis(coords,self.c)
		global ringi
		ringn=(r-self.parent.r+(ringi/2))//ringi
		newr=self.parent.r+(ringn*ringi)
		if ringn==0: return [self.c[0],self.c[1],newr]
		if abs(newr-r)>=10: return [self.c[0],self.c[1],newr]
		for cir in self.l:
			if (get_dis([cir[0],cir[1]],coords) < cir[2]-1):
				cir_r=get_dis([cir[0],cir[1]],self.c)
				if abs(cir_r-r)<10:
					
					return cir
		return []
	
	def findfree(self,coords):
		pass
		
	
class MenuIcon(Widget):
	#spawns moving icon on touch
	def __init__(self, **kwargs):
		super(MenuIcon,self).__init__(**kwargs)
		self.local_c=[0,0]
		self.r=30
		if kwargs is not None:
			for key, value in kwargs.items():
				if(key=='pos'): self.local_c=value
		self.icon=InstructionGroup()
		self.icon.add(Color(1,1,1))
		self.icon.add(Ellipse(size=(2*self.r,2*self.r),pos=(self.local_c[0]-self.r,self.local_c[1]-self.r)))
		self.icon.add(SmoothLine(circle=(self.local_c[0],self.local_c[1],self.r+4),width=3))
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(SmoothLine(circle=(self.local_c[0],self.local_c[1],self.r),width=3))
		for group in [self.icon]:
			self.canvas.add(group)
			
	def options(self):
		pass
	
	def on_touch_down(self,touch):
		if get_dis(self.local_c,touch.pos) < 40:
			a=MovingIcon(pos=touch.pos)
			a.init(self.r*.8)
			self.parent.add_widget(a)#adds moving icon to screen

class MenuCircle(Widget):
	#base of UI objects
	def __init__(self, **kwargs):
		super(MenuCircle, self).__init__(**kwargs)
		global c
		self.icons=[]
		self.connectors=[]
		self.r=100
		r=self.r
		self.pos=[c[0]-r,c[1]-r]
		self.local_c=c
		options=["start_node", "time", "variables","flow control","network","I/O","Sound/Notifications", "Interface"]
		with self.canvas:
			Color(.3,.3,.3)
			SmoothLine(circle=(c[0],c[1],r),width=3)
		mi=MenuIcon(pos=pol_to_car([r,90]))
		self.add_widget(mi)

class Test(Widget):
	#helper class to test functionality. remove from final disign
	def __init__(self, **kwargs): #test listofshapes()
		super(Test, self).__init__(**kwargs)
		global inuse
		inuse=[[100,100,20],[150,300,100],[500,200,60],[150,150,20],[700,600,200]]
		l=listofshapes(10)
		with self.canvas:
			Color(.3,.3,.3)
			for each in inuse:
				SmoothLine(circle=(each[0],each[1],each[2]),width=3)
			i=0.0
			for a in l:
				Color(i,.5,.5)
				i+=.5
				for each in a:
					Color(i,.5,.5)
					SmoothLine(circle=(each[0],each[1],each[2]),width=1)
		
class MagScreen(FloatLayout):
	def __init__(self, **kwargs):
		super(MagScreen, self).__init__(**kwargs)
		self.size=Window.size
		mc=MenuCircle()
		self.add_widget(mc)
		# ~ test=Test()
		# ~ self.add_widget(test)
		#make background with markers

class Magiscript(App):
	def build(self):
		self.layout=MagScreen()
		
		return self.layout
		
if __name__ == '__main__':
	Config.set('graphics','window_state','visible')
	Window.clearcolor=(1,1,1,1)
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
