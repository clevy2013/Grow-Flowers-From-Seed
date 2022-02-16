#TODO
	#Convert each petal to an image, create ability to overlay petals, change alpha, sat, and brightness, and change location for creation of extra petals. 
	#https://www.tutorialspoint.com/how-can-i-vary-a-shape-s-alpha-with-tkinter

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk  # Python 2
import random
import math


#Set Display Variables
WIDTH, HEIGHT = 900, 700

#Set Default Plant Genetics
def _seed_DefaultPlant():
	#Set Genetics
	GENES={"petal_num":8, "petal_rad":50, "petal_xFact":25, "petal_line": "#b5e3af", "petal_fill":"#D773A2", "petal_linewid":2, "petal_coeff":5,
	"center_line":"#b2b2ff", "center_fill":"#72c6ff", "center_linewid":4,"center_rad":25, "center_stipple":"",
	"layer_num":3, "layer_coeff":5,
	}
	GENES["center_rad"]=round(GENES["petal_rad"]/10)	
	
	#Set Heritability
	HERIT={"petal_num":0.5, "petal_rad":0.5, "petal_xFact":0.5, "petal_line": 0.5, "petal_fill":0.5, "petal_linewid":0.5, "petal_coeff":0.5,
	"center_line":0.5, "center_fill":0.5, "center_linewid":0.5,"center_rad":0.5, "center_stipple":"",
	"layer_num":0.5, "layer_coeff":0.5,
	}
	return GENES

def create_Colors(start='ABCDEF0123456789'):
	#TODO if bright add FFF if dark add 000
	rand_colors = ["#"+''.join([random.choice(start) for i in range(6)])]
	return rand_colors

def create_Reason(genes):
	while genes["petal_num"]<3:
		genes["petal_num"] += random.randint(1, 3)
	while genes["petal_rad"] <= 5*(genes["center_rad"] + genes["center_linewid"]):
		genes["petal_rad"] += random.randint(1, 12)
	while genes["center_rad"]<1:
		genes["center_rad"] += random.randint(1, 3)
	while genes["petal_xFact"]>100: 
		genes["petal_xFact"]-= random.randint(1, 30)
	while genes["center_rad"] < 2*genes["center_linewid"]:
		genes["center_rad"]+= random.randint(1, 40)
	while genes["layer_num"] <=0:
		genes["layer_num"]+= random.randint(1, 2)
	while genes["petal_coeff"] <=0:
		genes["petal_coeff"]+= random.randint(1, 10)
	return genes

def _seed_RandomPlant():
	genes = _seed_DefaultPlant()
	for key, value in genes.items():
		if isinstance(value, int):
			newval=random.weibullvariate(value, 1)
			newval=round(newval)
			newval=int(newval)
			genes.update({key:newval})
		else:
			genes.update({key:create_Colors()})
		genes = create_Reason(genes)
	return genes

def _seed_SelfedPlant(genes, heritability):
	for key, value in genes.items():
		if isinstance(value, int):
			newval=random.weibullvariate(value, value*heritability)
			newval=round(newval)
			newval=int(newval)
			genes[key]=newval
		else: 
			genes[key]=create_Colors(start=value[1:])
	return genes

def _create_Circle( x, y, r, **kwargs):
	return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_Circle = _create_Circle

def _create_Petals( x, y, petal_num, radius, xFactor, coefficent, **kwargs):
	points = []
	for degrees in range(0, 360-xFactor):
		radians = math.radians(degrees)
		distance = math.sin(radians * petal_num) * radius
		points.append(x+math.cos(coefficent*radians) * distance)
		points.append(y+math.sin(coefficent*radians) * distance)
	return canvas.create_polygon(points,smooth=0, **kwargs)
tk.Canvas.create_Petals = _create_Petals

def _create_Flowers( bud_x, bud_y, genes):
	for l in range(genes["layer_num"]):
		canvas.create_Petals(bud_x, bud_y, 
					petal_num=genes["petal_num"], radius=genes["petal_rad"], xFactor=genes["petal_xFact"], coefficent=genes["petal_coeff"],  
					fill=genes["petal_fill"], outline=genes["petal_line"], width=genes["petal_linewid"])
		canvas.create_Circle(bud_x, bud_y, r=genes["center_rad"],
				fill=genes["center_fill"], outline=genes["center_line"], 
				width=genes["center_linewid"]) # stipple=genes["center_stipple"]
tk.Canvas.create_Flowers = _create_Flowers

def _create_Stems(x, y, thickness, height, angle, branches):
	points = [x, y]
	print(height)
	print(thickness)
	#points += [x, y2, x2, y]
	#self.create_polygon(points)

	""" 
	if depth >= 0:
		depth -= 1
		thickness -= thickness/depth
		x2 = x + int(math.cos(angle) * height)
		y2 = y - int(math.sin(angle) * height)

		# Draw the line
		self.create_line(x1,y1, x2,y2, width=thickness)
		
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
		print("Experienced an Error")
		genes = _seed_DefaultPlant()

	flower_num=1	
	bud_x = [random.randint(10, WIDTH-10)]
	bud_y = [random.randint(10, HEIGHT-10)]

	#create_Stems(x = bud_x, y = bud_y, thickness=10, height=40,  angle=60, branches=1)

	for i in range(flower_num):
		create_Flowers(bud_x[i], bud_y[i], genes)

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