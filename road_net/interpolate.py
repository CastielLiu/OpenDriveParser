
# -*-coding=utf-8-*-

import numpy as np
import math
import matplotlib.pyplot as plt
import os
import sys

class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.yaw = 0
		self.curvature = 0

def distance(p1,p2):
	delta_x = p2.x - p1.x
	delta_y = p2.y - p1.y
	return math.sqrt(delta_x*delta_x+delta_y*delta_y)

def interpolate(input_points):
	output_points = []
	length = len(input_points)
	for i in range(1,length):
		delta_x = input_points[i].x - input_points[i-1].x
		delta_y = input_points[i].y - input_points[i-1].y
		
		yaw = math.atan2(delta_x,delta_y)
		dis = math.sqrt(delta_x*delta_x+delta_y*delta_y)
		
		if(dis > 0.1):
			cnt = int(round(dis/0.1))
			increment_x = (delta_x)/cnt
			increment_y = (input_points[i].y - input_points[i-1].y)/cnt
			for j in range(1, cnt):
				point = Point(input_points[i-1].x+increment_x*j, input_points[i-1].y+increment_y*j)
				point.yaw = yaw
				output_points.append(point)
		input_points[i].yaw = yaw
		output_points.append(input_points[i])
	return output_points

def dumpPoints(file_name, points):
	with open(file_name,'w') as f:
		for point in points:
			f.write('%.3f\t%.3f\t%.3f\n' %(point.x,point.y,point.yaw))

def main(argv):
	if(len(argv) <2):
		print("please input file name")
		return
	points = []
	with open(argv[1],'r') as f:
		while True:
			line = f.readline()
			if(len(line) == 0):
				break
			data = line.split()
			point = Point(float(data[0]),float(data[1]))
			points.append(point)
	
	points = interpolate(points)
	
	if(len(argv) == 3):
		dumpPoints(argv[2],points)
	
	xs = [point.x for point in points]
	ys = [point.y for point in points]
	yaws = [point.yaw for point in points]

	plt.plot(xs, ys, 'r-')
	plt.axis('equal')
	plt.show()

if __name__ == "__main__":
	main(sys.argv)
