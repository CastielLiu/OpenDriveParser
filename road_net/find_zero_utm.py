# -*-coding=utf-8-*-

import numpy as np
import math
import matplotlib.pyplot as plt
import os
import sys

def loadPoints(file_name,offset_x=0,offset_y=0):
	points = []
	with open(file_name,'r') as f:
		while True:
			line = f.readline()
			if(len(line) == 0):
				break
			data = line.split()
			x = float(data[0])+offset_x
			y = float(data[1])+offset_y
			points.append([x,y])
	return points

def offsetPoints(points,offset_x=0,offset_y=0):
	for i in range(len(points)):
		points[i][0] = points[i][0] + offset_x
		points[i][1] = points[i][1] + offset_y
	return points

def rotation(points,angle):
	theta = angle/180.0*math.pi
	cnt = 0
	for point in points:
		x = point[0]
		y = point[1]
		points[cnt][0] = x * math.cos(theta) + y * math.sin(theta)
		points[cnt][1] = -x* math.sin(theta) + y * math.cos(theta)
		cnt = cnt + 1
	return points

def main(argv):
	
	points1 = loadPoints("tulu.txt")
	delta_x = 0
	delta_y = 2.0
	points2 = loadPoints("R31.txt")
	points2 = rotation(points2,1.3)
	points2 = offsetPoints(points2, 288477.894+delta_x, 3496772.181+delta_y)
	
	points1 = np.array(points1)
	points2 = np.array(points2)
	plt.plot(points1[:,0],points1[:,1],'r-',label="true")
	plt.plot(points2[:,0],points2[:,1],'b-',label="false")
	plt.legend()
	plt.axis('equal')
	plt.show()

if __name__ == "__main__":
	main(sys.argv)
