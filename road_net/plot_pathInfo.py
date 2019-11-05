
# -*-coding=utf-8-*-

import numpy as np
import math
import matplotlib.pyplot as plt
import os

def drawRoad(road_file):
	points = []
	with open(road_file,'r') as f:
		while True:
			line = f.readline()
			if(len(line) == 0):
				break
			x,y,z = line.split()
			x = float(x)
			y = float(y)
			points.append([x,y])

	points = np.array(points)


	plt.plot(points[:,0],points[:,1],'r-*')
	plt.axis('equal')
	
	
path = "pathInfo/"
dirs = os.listdir(path)
for _file in dirs:
	drawRoad(path + _file)
plt.show()





