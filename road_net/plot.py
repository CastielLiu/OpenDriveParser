
# -*-coding=utf-8-*-

import numpy as np
import math
import matplotlib.pyplot as plt
import os


points = []

with open("map.txt",'r') as f:
	while True:
		line = f.readline()
		if(len(line) == 0):
			break
		x,y,z = line.split()
		x = float(x)
		y = float(y)
		points.append([x,y])

points = np.array(points)

#plt.plot(points[:12,0],points[:12,1],'r-*')
#plt.plot(points[13:,0],points[13:,1],'b-*')
#plt.plot(points[:3,0],points[:3,1],'b-*')
#plt.plot(points[3:6,0],points[3:6,1],'r-*')
#plt.plot(points[6:,0],points[6:,1],'k-*')
plt.plot(points[:,0],points[:,1],'r*')
plt.axis('equal')
plt.show()
		
