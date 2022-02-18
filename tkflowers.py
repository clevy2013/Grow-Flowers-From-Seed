#TODO
	#Convert each petal to an image, create ability to overlay petals, change alpha, sat, and brightness, and change location for creation of extra petals. 
	#https://www.tutorialspoint.com/how-can-i-vary-a-shape-s-alpha-with-tkinter

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk  # Python 2
import random
import math
from statistics import mean

#Set Display Variables
WIDTH, HEIGHT = 900, 700

#Set Default Plant Genetics
def _seed_DefaultPlant():
	#Set Genetics
	GENES={"petal_num":7, "petal_rad":80.0, "petal_xFact":2, "petal_line": "#b5e3af", "petal_fill":"#D773A2", "petal_linewid":2.0, "petal_coeff":6,
	"center_line":"#b2b2ff", "center_fill":"#72c6ff", "center_linewid":1.0,"center_rad":5.0, "center_stipple":"",
	"layer_num":1, "layer_coeff":2.0}
	GENES["center_rad"]=round(GENES["petal_rad"]/10)	
	
	#Set Heritability
	HERIT={"petal_num":0.5, "petal_rad":0.5, "petal_xFact":0.5, "petal_line": 0.5, "petal_fill":0.5, "petal_linewid":0.5, "petal_coeff":0.5,
	"center_line":0.5, "center_fill":0.5, "center_linewid":0.5,"center_rad":0.5, "center_stipple":"",
	"layer_num":0.5, "layer_coeff":0.5}
	return GENES

def create_Colors(start='ABCDEF0123456789'):
	#TODO if bright add FFF if dark add 000
	rand_colors = ["#"+''.join([random.choice(start) for i in range(6)])]
	return rand_colors

def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i

def create_Lines(x1, y1, x2, y2, wave_height = 10, wave_length = 50, curveSquaring = .1):

	assert 0 <= curveSquaring <= 1, 'curveSquaring should be a value between 0 and 1: {}'.format(curveSquaring)
	assert wave_length > 0, 'wavelength smaller or equal to zero: {}'.format(wave_length)

	diagonal = math.sqrt((x1 - x2)**2 + (y1 - y2)**2) 
	angle = math.atan2((y2-y1), (x2-x1)) # radians
	wave_n = diagonal//int(wave_length) #number of waves
	wave_i = diagonal/float(wave_n) #interval of waves
	bez_ml = math.sqrt((wave_i/4.)**2+wave_height/2.)**2 #max bezier curve point length
	bez_l = bez_ml*curveSquaring #bezier length
	bez_i = math.atan2((wave_height/2.-0), (wave_i/4.-0)) #bezier inclination	
	
	points_wiggly = [x1, y1]
	flexpt = [x1, y1]
	polarity = 1

	for waveIndex in range(0, int(wave_n*5)):
		bez_oa = angle+bez_i*polarity #Bezier out angle 
		bez_os = [flexpt[0]+math.cos(bez_oa)*bez_l, flexpt[1]+math.sin(bez_oa)*bez_l] #bezier outside
		flexpt = [flexpt[0]+math.cos(angle)*wave_i/2., flexpt[1]+math.sin(angle)*wave_i/2.]
		bez_ia = angle+(math.radians(180)-bez_i)*polarity #bezier interior angle
		bez_in = [flexpt[0]+math.cos(bez_ia)*bez_l, flexpt[1]+math.sin(bez_ia)*bez_l] #bezier interiro
		
		points_wiggly += [bez_os, bez_in, flexpt]
		points_wiggly += bez_in
		points_wiggly += flexpt

		polarity *= -1
	return points_wiggly
	

def create_Reason(genes):
	while genes["petal_num"]<3:
		genes["petal_num"] += random.randint(1, 5)
	while genes["petal_rad"] <= 5*(genes["center_rad"] + genes["center_linewid"]):
		genes["petal_rad"] += random.randint(1, 12)
	while genes["petal_xFact"]>100: 
		genes["petal_xFact"]-= random.randint(1, 30)
	while genes["center_rad"] < 2*genes["center_linewid"]:
		genes["center_rad"]+= random.randint(1, 40)
	while genes["layer_num"] <=0:
		genes["layer_num"]+= random.randint(1, 2)
	return genes

def _seed_RandomPlant():
	genes = _seed_DefaultPlant()
	for key, value in genes.items():
		if isinstance(value, int):
			newval=random.weibullvariate(value, 1)
			newval=math.ceil(newval)
			newval=int(abs(newval))
			genes.update({key:newval})
		elif isinstance(value, float):
			newval=random.weibullvariate(value, 1)
			newval=float(abs(newval))
			genes.update({key:newval})
		elif isinstance(value, bool):
			newval=random.randchoice(True, False)
			genes.update({key:newval})
		elif isinstance(value, str): 
			newval=create_Colors()	
			genes.update({key:newval})	
	genes = create_Reason(genes)
	return genes

def _seed_SelfedPlant(genes, heritability):
	for key, value in genes.items():
		if isinstance(value, int):
			newval=random.weibullvariate(value, value*heritability)
			newval=round(newval)
			newval=int(newval)
			genes[key]=newval
		elif isinstance(value, float):
			newval=random.weibullvariate(value, value*heritability)
			genes[key]=newval
		elif isinstance(value, boolean):
			genes[key]=random.randchoice(True, False)
		elif isinstance(value, string): 
			genes[key]=create_Colors(start=value[1:])
	return genes

def _create_Circle(self, x, y, r, **kwargs):
	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_Circle = _create_Circle

def _create_Petals(self, x, y, petal_num, radius, xFactor, coefficent, **kwargs):
	points = []
	for degrees in range(0, 360-xFactor):
		radians = math.radians(degrees)
		distance = math.sin(radians * petal_num) * radius
		points.append(x+math.cos(coefficent*radians) * distance)
		points.append(y+math.sin(coefficent*radians) * distance)
	return self.create_polygon(points,smooth=0, **kwargs)
tk.Canvas.create_Petals = _create_Petals

def _create_Flowers(self, bud_x, bud_y, genes):
	for l in range(genes["layer_num"]):
		self.create_Petals(bud_x, bud_y, 
					petal_num=genes["petal_num"], radius=genes["petal_rad"], xFactor=genes["petal_xFact"], coefficent=genes["petal_coeff"],  
					fill=genes["petal_fill"], outline=genes["petal_line"], width=genes["petal_linewid"])
		self.create_Circle(bud_x, bud_y, r=genes["center_rad"],
				fill=genes["center_fill"], outline=genes["center_line"], 
				width=genes["center_linewid"]) # stipple=genes["center_stipple"]
tk.Canvas.create_Flowers = _create_Flowers

def _create_Stems(self, x, y, base_x, base_y, thickness, height, angle, branches):
	points = [] #[base_x-thickness, base_y, base_x+thickness, base_y]
	points += create_Lines(x, y, base_x-thickness, base_y)
	#points += create_Lines(x, y, base_x+thickness, base_y)
	print(points)
	self.create_line(points)

	""" 
	if depth >= 0:
		depth -= 1
		thickness -= thickness/depth
		x2 = x + int(math.cos(angle) * height)
		y2 = y - int(math.sin(angle) * height)

		# Draw the line
		self.create_line(x1,y1, x2,y2, width=thickness, fill = "white")
		
		# Draw the left branch
		self.paintBranch(depth, x2, y2, length * self.sizeFactor, angle + self.angleFactor  )
		# Draw the right branch
            	self.paintBranch(depth, x2, y2, length * self.sizeFactor, angle - self.angleFactor )  
	"""       
	canvas.create_polygon(points)
tk.Canvas.create_Stems = _create_Stems
	

if __name__ == '__main__':
	root = tk.Tk()
	canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
	canvas.grid()

	try:
		genes = _seed_RandomPlant()
	except:
		genes = _seed_DefaultPlant()

	flower_num=1	
	bud_x = [random.randint(10, WIDTH-10) for i in range(flower_num) ]
	bud_y = [random.randint(10, HEIGHT-10) for i in range(flower_num) ]
	base_x = WIDTH/2
	base_y = HEIGHT
	
	for i in range(flower_num):
		canvas.create_Stems(bud_x[i], bud_y[i], base_x, base_y,
			thickness=10, height=40,  angle=60, branches=1)
		canvas.create_Flowers(bud_x[i], bud_y[i], genes)

	root.mainloop()

"""
def _seed_BredPlants(genes1, genes2):
	gene=dict()
	for gene1, gene2 in zip(genes1.values(), genes2.values()) :
		if isinstance(gene, int):
			gene=random.choice(gene1, gene2, mean(gene1, gene2), random.gauss(mean(gene1, gene2)))
		else:
			gene=create_Colors(start=gene1[1:]+gene2[1:])
	return genes



"""