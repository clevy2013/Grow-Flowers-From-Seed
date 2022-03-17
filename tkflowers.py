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

#Simple Functions
def create_Colors(start='ABCDEF0123456789'):
	rand_colors = ["#"+''.join([random.choice(start) for i in range(6)])]
	return rand_colors
def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i
        

#Grow My Plants

class phenotype:
        def __init__(self, petal_num, petal_rad, petal_xFact, petal_line, petal_fill, petal_linewid, petal_coeff,
                     center_rad, center_line, center_fill, center_linewid, center_stipple,
                     layer_num, layer_coeff):
                self.petal_num = petal_num
                self.petal_rad = petal_rad
                self.petal_xFact = petal_xFact
                self.petal_line = petal_line
                self.petal_fill = petal_fill
                self.petal_linewid = petal_linewid
                self.petal_coeff = petal_coeff
                self.center_rad =  center_rad
                self.center_line = center_line
                self.center_fill = center_fill
                self.center_linewid = center_linewid
                self.center_stipple = center_stipple
                self.layer_num = layer_num
                self.layer_coeff = layer_coeff
class parent1:
        def __init__(self, placehold):
                placehold = placehold     
class parent2:
        def __init__(self, placehold):
                placehold = placehold      
class expression:
        def __init__(self, placehold):
                placehold = placehold     
class heritability:
        def __init__(self, placehold):
                placehold = placehold  

class SeedAPlant:
        def __init__(self, phenotype, parent1, parent2, expression, heritability):
                self.phenotype=phenotype
                self.parent1 = parent1
                self.parent2 = parent2
                self.expression = expression
                self.heritability = heritability
                     
        def Random(self, phenotype, parent1, parent2, expression, heritability):
                phenotype.petal_num = random.randint(phenotype.petal_num[1], phenotype.petal_num[2])
                phenotype.petal_rad = random.randint(phenotype.petal_rad[1], phenotype.petal_rad[2])
                phenotype.petal_xFact = random.randint(phenotype.petal_xFact[1], phenotype.petal_xFact[2])
                phenotype.petal_line = create_Colors(phenotype.petal_line)
                phenotype.petal_fill = create_Colors(phenotype.petal_fill)
                phenotype.petal_linewid = random.uniform(phenotype.petal_linewid[1], phenotype.petal_linewid[2])
                phenotype.petal_coeff = random.randint(phenotype.petal_coeff[1], phenotype.petal_coeff[2])
                phenotype.center_rad =  random.randint(phenotype.center_rad[1], phenotype.center_rad[2])
                phenotype.center_line = create_Colors(phenotype.center_line)
                phenotype.center_fill = create_Colors(phenotype.center_fill)
                phenotype.center_linewid = random.uniform(phenotype.center_linewid[1], phenotype.center_linewid[2])
                phenotype.center_stipple = create_Colors(phenotype.center_stipple)
                phenotype.layer_num = random.randint(phenotype.layer_num[1], phenotype.layer_num[2])
                phenotype.layer_coeff = random.uniform(phenotype.layer_coeff[1], phenotype.layer_coeff[2])

def Crossed(parent1, parent2):
       newplant = DefaultPlant()
       newplant.phenotype
       newplant.parent1 = parent1.phenotype
       newplant.parent2 = parent2.phenotype
       newplant.expression #random.choice(parent1.expression, parent2.expression)
       newplant.heritability #random.randbetween(random.gauss(parent1.heritability, .1), random.gauss(parent2.heritability, .1))
       return newplant
       
def SelfedPlant():
       newplant = DefaultPlant()
       newplant.phenotype
       newplant.parent1 = parent1.phenotype
       newplant.parent2 = []
       newplant.expression #random.choice(parent1.expression)
       newplant.heritability #random.gauss(parent1.heritability, .1)
       return newplant

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

def _create_Flowers(self, bud_x, bud_y, seed):
        phenotype=seed.phenotype
        for l in range(phenotype.layer_num[0]):
                self.create_Petals(bud_x, bud_y, phenotype.petal_num[0], radius=phenotype.petal_rad[0], xFactor=phenotype.petal_xFact[0], coefficent=phenotype.petal_coeff[0], fill=phenotype.petal_fill[0], outline=phenotype.petal_line[0], width=phenotype.petal_linewid[0])
                self.create_Circle(bud_x, bud_y, r=phenotype.center_rad[0], fill=phenotype.center_fill[0], outline=phenotype.center_line[0], width=phenotype.center_linewid[0]) # stipple=phenotype.center_stipple
tk.Canvas.create_Flowers = _create_Flowers

def _create_Stems(self, x, y, base_x, base_y, thickness, height, angle, branches):
	points = [] #[base_x-thickness, base_y, base_x+thickness, base_y]
	points += create_Lines(x, y, base_x-thickness, base_y)
	self.create_line(points)
	canvas.create_polygon(points)
tk.Canvas.create_Stems = _create_Stems

#Import Plant Seeds
seed_default = (phenotype([7, 3, 10], [80.0, 10.0, 100.0], [2, 0, 10], ["#b5e3af"], ["#D773A2"], [2.0, 0.0, 50.0], [6, 0, 180],
        [8, 0, 50], ["#b2b2ff"], ["#72c6ff"], [1.0, 0.0, 50.0], ["#b2b2ff"],
        [1, 1, 10], [2.0, 0, 5.0]),
                parent1(1),
                parent2(1),
                expression(1),
                heritability(1))	

if __name__ == '__main__':
	root = tk.Tk()
	canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
	canvas.grid()

	try:
                NewSeed = SeedAPlant.Random(seed_default[0], seed_default[1], seed_default[2], seed_default[3], seed_default[4])
	except Exception as e:
                print(e)
                NewSeed = SeedAPlant(seed_default[0], seed_default[1], seed_default[2], seed_default[3], seed_default[4])

	flower_num=1	
	bud_x = [random.randint(10, WIDTH-10) for i in range(flower_num) ]
	bud_y = [random.randint(10, HEIGHT-10) for i in range(flower_num) ]
	base_x = WIDTH/2
	base_y = HEIGHT
	
	for i in range(flower_num):
		canvas.create_Stems(bud_x[i], bud_y[i], base_x, base_y,
			thickness=10, height=40,  angle=60, branches=1)
		canvas.create_Flowers(bud_x[i], bud_y[i], NewSeed)

	root.mainloop()

