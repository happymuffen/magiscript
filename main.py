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

#add drawpercentage() to all visible classes for animating loading saves

class point():
	def __init__(self,a,b,pnt=None):#takes x and y or r,t, and pnt
		global c
		if pnt==None:#takes x and y
			self.x,self.y=a,b
			if c==None:
				self.r,self.t=0.0,0.0
				self.local_r,self.local_t= None,None
			else:
				self.r,self.t=self.car_to_pol([a,b],c)
				self.local_r,self.local_t= self.car_to_pol([self.x,self.y],c)
				self.center=c
		else:#takes r,t, and a relative center point
			self.local_r,self.local_t= a,b
			self.x,self.y=self.pol_to_car([a,b],pnt)
			self.r,self.t=self.r,self.t=self.car_to_pol([self.x,self.y],c)
			self.center=pnt
	
	def __str__(self):
		return "Cartisian: %s\nPolar: %s" %([self.x,self.y],[self.local_r,self.local_t])
		
	def __eq__(self, other):
		if not isinstance(other, point):
			# don't attempt to compare against unrelated types
			return NotImplemented
		return self.x==other.x and self.y==other.y
		
	def car_to_pol(self,car,c):
		#gets polar coords relative to center from cartisian [r,t]
		dx=car[0]-c.x
		#can't divide by 0
		if dx==0:
			dx=.0000000000000000001
		#atan(x) only outputs +/-180
		b=0
		if dx<0:
			b=180
		pol= [get_dis([c.x,c.y],car), math.degrees(math.atan((car[1]-c.y)/dx))+b]
		if pol[1]<0:
			pol[1]+=360
		return pol
	
	def pol_to_car(self,pol,c):
		#gets cartisian coords to polar from center [x,y]
		car= [pol[0]*math.cos(math.radians(pol[1]))+c.x, pol[0]*math.sin(math.radians(pol[1]))+c.y]
		return car
			
	def coords(self): #returns [x,y]
		return [self.x,self.y]
	def polar(self): #returns [r,theta]
		return [self.r,self.t]
	
	def move_to(self,coords):
		self.x,self.y=coords[0],coords[1]
		global c
		self.r,self.t=self.car_to_pol([self.x,self.y],c)
		self.local_r,self.local_t= self.car_to_pol([self.x,self.y],self.center)
	
	def set_local(self,point):
		self.center=point
		self.local_r,self.local_t= self.car_to_pol([self.x,self.y],point)
	
class circle():#takes point and r
	def __init__(self,c,r):
		self.c,self.r=c,r
		
	def move_to(self, pnt):
		self.c=pnt
			
c=None
c=point(Window.center[0],Window.center[1])
print(repr(c))
ringi=110
inuse=[]
buf=(100+ringi)*math.pi/6

def get_dis(c1,c2):
	#returns the distance between two lists of cartisian coordanites
	return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)

def get_dis_pnt(p1,p2):
	#returns the distance between two points
	return math.sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)

def pol_to_car(pol,c):
	#gets cartisian coords to polar from center [x,y]
	car= [pol[0]*math.cos(math.radians(pol[1]))+c.x, pol[0]*math.sin(math.radians(pol[1]))+c.y]
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
		l.append([each.c.x,each.c.y,r+buf+each.r])
	return l
					
def makepoint(coords,canvas):
	canvas.add(Color(1,0,0))
	canvas.add(SmoothLine(circle=(coords[0],coords[1],2),width=3))
	
	
def intersects(cir0,cir1):
	#tests for intersections in two circles quickly
	d=get_dis_pnt(cir0.c,cir1.c)
	if cir0.r+cir1.r < d:return 0#seperate circles
	if cir1.r-cir0.r > d: return -1#the first is inside the second
	if cir0.r-cir1.r > d: return -2#the second is inside the first
	if cir0.r-cir1.r ==d: return -3#intersection at 1 point(or same circle)
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
		
	def init(self,pnt1,coords):
		self.pnt1=pnt1
		self.canvas.opacity=.2
		pnt=point(coords[0],coords[1])
		pnt=self.limitpos(pnt)
		pnt.set_local(self.pnt1)
		self.canvas.add(SmoothLine(circle=(self.pnt1.x,self.pnt1.y,33,120-pnt.local_t,60-pnt.local_t),width=3))
		
	def draw(self,path):
		self.canvas.clear()
		for group in [path]:
			self.canvas.add(group)
			
	
	
	def on_touch_move(self,touch):
		if self.pnt1==None: return
		l=touch.pos
		pnt=point(l[0],l[1])
		pnt=self.limitpos(pnt)
		pnt.set_local(self.pnt1)
		path=InstructionGroup()
		if get_dis_pnt(self.pnt1,pnt)>35:
			self.makepath(path,pnt)
		
		path.add(SmoothLine(circle=(self.pnt1.x,self.pnt1.y,33,120-pnt.local_t,60-pnt.local_t),width=3))
		self.draw(path)
	
	def on_touch_up(self,touch):
		
		self.parent.remove_widget(self)
	
	
	
	def limitpos(self,pnt):
		#should find snap location for pnt
		return pnt
	
	def makepath(self,todraw,pnt):
		#returns InstructionGroup containing all relevent things to draw.
		pnt=self.limitpos(pnt)
		tmppnt=point(35.5,pnt.local_t,self.pnt1)
		todraw.add(SmoothLine(points=[tmppnt.x,tmppnt.y,pnt.x,pnt.y],cap='round', joint='round', width=3))
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
				if(key=='pos'): local_c=value
		c=point(value[0],value[1])
		self.cir=circle(c,30)
		self.click=False
		self.time=-1
		
	def makeicon(self,r):
		self.cir.r=r
		global inuse
		inuse.append(self.cir)
		
		self.canvas.clear()
		self.icon=InstructionGroup()
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(Color(1,1,1))
		self.icon.add(Ellipse(size=(2*self.cir.r,2*self.cir.r),pos=(self.cir.c.x-self.cir.r,self.cir.c.y-self.cir.r)))
		self.icon.add(SmoothLine(circle=(self.cir.c.x,self.cir.c.y,self.cir.r+4),width=3))
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(SmoothLine(circle=(self.cir.c.x,self.cir.c.y,self.cir.r),width=3))
		for group in [self.icon]:
			self.canvas.add(group)	
	
	def now(self):
		now=datetime.datetime.now()
		return int(now.strftime("%M"))*60+int(now.strftime("%s"))
	
	def on_touch_down(self,touch):
		if get_dis(self.cir.c.coords(),touch.pos) < self.cir.r:
			self.click=True
			self.time=self.now()
			#test for click&drag
			#test for connecting
	
	def on_touch_move(self,touch):
		if self.click:
			if self.time<0:
				global inuse
				try:
					inuse.remove(self.cir)
				except ValueError:
					pass
				
				a=MovingIcon(pos=touch.pos)
				a.init(self.cir.r)
				self.parent.add_widget(a)#adds moving icon to screen
				self.parent.remove_widget(self)
			else:
				time=self.now()
				if self.time>time:#edge case of hour ticks over
					time+=3600
				if time-self.time>0:
					a=MovingConector()
					a.init(self.cir.c,touch.pos)
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
		local_c=point(0,0)
		self.pointslist=[]
		if kwargs is not None:
			for key, value in kwargs.items():
				if(key=='pos'): local_c=point(value[0],value[1])
		self.cir=circle(local_c,24)
	
	def makepoint(self,coords):
		self.pointslist.append(coords)
		
	def init(self,r):
		self.l=listofshapes(r)
		self.r=r
		self.updateloc(self.cir.c)
	
	def updateloc(self, coords):
		self.cir.move_to(coords)
		self.canvas.clear()
		self.icon=InstructionGroup()
		self.canvas.opacity=.2		
		self.icon.add(Color(1,1,1))
		self.icon.add(Ellipse(size=(2*self.cir.r,2*self.cir.r),pos=(self.cir.c.x-self.cir.r,self.cir.c.y-self.cir.r)))
		self.icon.add(SmoothLine(circle=(self.cir.c.x,self.cir.c.y,self.cir.r+4),width=3))
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(SmoothLine(circle=(self.cir.c.x,self.cir.c.y,self.cir.r),width=3))
		for group in [self.icon]:
			self.canvas.add(group)
		
		#handles makepoint
		if len(self.pointslist)>0:
			self.canvas.add(Color(.1,.1,.1))
			for each in self.pointslist:
				self.canvas.add(SmoothLine(circle=(each.x,each.y,5),width=1))
			self.pointslist=[]
			
	def on_touch_move(self, touch):
		pnt=point(touch.pos[0],touch.pos[1])
		l=self.limitpos(pnt)
		self.updateloc(l)
	
	def limitpos(self,pnt):
		self.makepoint(pnt)
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
		
		#snap if within 50
		
		#sort function for finding the shortest distance between coords
		# ~ def sort_by_d(arr,pnt):
			# ~ if arr==[[]]: return []
			# ~ def itersort_d(lh):
				# ~ l=lh[0]
				# ~ h=lh[1]
				# ~ p=l
				# ~ ldist=get_dis(arr[l],coords)
				# ~ for i in range(l+1,h):
					# ~ if get_dis(arr[i],coords)<ldist:
						# ~ p+=1
						# ~ arr[p],arr[i] = arr[i],arr[p]
				# ~ arr[p], arr[l]= arr[l],arr[p]
				# ~ return [l,p,h]
			# ~ pars=[[0,len(arr)]]
			# ~ while len(pars)>0:
				# ~ newpars=[]
				# ~ for each in pars:
					# ~ o=itersort_d(each)
					# ~ l,p,h=o[0],o[1],o[2]
					# ~ if not p-l<=1:newpars.append([l,p])
					# ~ if not h-p<=1:newpars.append([p+1,h])
				# ~ pars=newpars
			# ~ return arr
		
		#preset locations
		#spider patern
		
		pntcir=circle(pnt,50)
		testr=(pnt.r+35)//100*100
		if testr<150: return pnt
		testpnt=point(testr,(pnt.t+22)//45*45,self.c)
		testcir=circle(testpnt,1)
		if (intersects(pntcir,testcir)!=0)&(testpnt.local_r>150):
			#test if position is occupied
			global inuse
			for each in inuse:
				if each.c==testpnt: return pnt
			pnt=testpnt
	
		return pnt
	
	def on_touch_up(self,touch):
		if self.isgood(self.cir.c)==self.cir.c:
			a=ItemIcon(pos=self.cir.c.coords())
			a.makeicon(self.cir.r)
			self.parent.add_widget(a)
		self.parent.remove_widget(self)
	
	def isgood(self, pnt): #Returns pnt if pnt is good
		if (pnt.r<150) or (pnt.local_r%100>0) or (pnt.local_t%45>0): return None
		global inuse
		for each in inuse:
			if each.c==pnt: return None
		return pnt
	
	def findfree(self,coords):
		pass
		
	
class MenuIcon(Widget):
	#spawns moving icon on touch
	def __init__(self, **kwargs):
		super(MenuIcon,self).__init__(**kwargs)
		local_c=[0,0]
		if kwargs is not None:
			for key, value in kwargs.items():
				if(key=='pos'): local_c=value
		c=point(local_c[0],local_c[1])
		self.cir=circle(c,30)
		
		self.icon=InstructionGroup()
		self.icon.add(Color(1,1,1))
		self.icon.add(Ellipse(size=(2*self.cir.r,2*self.cir.r),pos=(c.x-self.cir.r,c.y-self.cir.r)))
		self.icon.add(SmoothLine(circle=(c.x,c.y,self.cir.r+4),width=3))
		self.icon.add(Color(.3,.3,.3))
		self.icon.add(SmoothLine(circle=(c.x,c.y,self.cir.r),width=3))
		for group in [self.icon]:
			self.canvas.add(group)
			
	def options(self):
		pass
	
	def on_touch_down(self,touch):
		if get_dis(self.cir.c.coords(),touch.pos) < 40:
			a=MovingIcon(pos=touch.pos)
			a.init(self.cir.r*.8)
			self.parent.add_widget(a)#adds moving icon to screen

class MenuCircle(Widget):
	#base of UI objects
	def __init__(self, **kwargs):
		super(MenuCircle, self).__init__(**kwargs)
		global c
		self.icons=[]
		self.connectors=[]
		r=100
		self.cir=circle(c,r)
		options=["start_node", "time", "variables","flow control","network","I/O","Sound/Notifications", "Interface"]
		with self.canvas:
			Color(.3,.3,.3)
			SmoothLine(circle=(c.x,c.y,r),width=3)
		mi=MenuIcon(pos=[self.cir.c.x,self.cir.c.y+r])
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
