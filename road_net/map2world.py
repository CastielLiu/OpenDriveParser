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
		self.max_speed = 100

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
			points.append(Point(x,y))
	return points

def offsetPoints(points,offset_x=0,offset_y=0):
	for i in range(len(points)):
		points[i].x = points[i].x + offset_x
		points[i].y = points[i].y + offset_y
	return points

def rotation(points,angle):
	theta = angle/180.0*math.pi
	cnt = 0
	for point in points:
		x = point.x
		y = point.y
		points[cnt].x = x * math.cos(theta) + y * math.sin(theta)
		points[cnt].y = -x* math.sin(theta) + y * math.cos(theta)
		cnt = cnt + 1
	return points

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
		
		dis = math.sqrt(delta_x*delta_x+delta_y*delta_y)
#		print(dis)
		if(dis > 0.1):
			cnt = int(round(dis/0.1))
			increment_x = (delta_x)/cnt
			increment_y = (input_points[i].y - input_points[i-1].y)/cnt
			for j in range(1, cnt):
				point = Point(input_points[i-1].x+increment_x*j, input_points[i-1].y+increment_y*j)
				if(dis <5.0):
					point.curvature = input_points[i-1].curvature
				output_points.append(point)
		output_points.append(input_points[i])
	return output_points

def dumpPoints(file_name, points):
	with open(file_name,'w') as f:
		for point in points:
			f.write('%.3f\t%.3f\t%d\t%.3f\n' %(point.x,point.y,0,point.curvature))
#			f.write('%.3f\t%.3f\t%d\t%.3f\t%.2f\n' %(point.x,point.y,0,point.curvature,point.max_speed))

def calculateRHO(points, index):
	if(index == 0 or index == len(points)-1):
		return 0
	x1 = points[index-1].x
	y1 = points[index-1].y
	
	x2 = points[index].x
	y2 = points[index].y
	
	x3 = points[index+1].x
	y3 = points[index+1].y
	
	A = x1*(y2-y3)-y1*(x2-x3)+x2*y3-x3*y2
	B = (x1*x1+y1*y1)*(y3-y2)+(x2*x2+y2*y2)*(y1-y3)+(x3*x3+y3*y3)*(y2-y1)
	C = (x1*x1+y1*y1)*(x2-x3)+(x2*x2+y2*y2)*(x3-x1)+(x3*x3+y3*y3)*(x1-x2)
	D = (x1*x1+y1*y1)*(x3*y2-x2*y3)+(x2*x2+y2*y2)*(x1*y3-x3*y1)+(x3*x3+y3*y3)*(x2*y1-x1*y2)
	
	return 2*A/math.sqrt(B*B+C*C-4*A*D)
	
def generateRHO(points):
	for i in range(1,len(points)):
		points[i].curvature = calculateRHO(points,i)
	return points
	
def generateMaxSpeed(points,max_a):
	for i in range(0,len(points)):
		cur = abs(points[i].curvature)
		if(cur < 0.001):
			continue
		points[i].max_speed = math.sqrt(1.0/cur*max_a) *3.6;
	return points
	

def main(argv):
	if(len(argv) <2):
		print("please input file name")
		return
	
	points = loadPoints(argv[1])
	points = generateRHO(points) #生成曲率
	points = rotation(points,1.3) #旋转
	delta_x = 0
	delta_y = 2.0
	points = offsetPoints(points, 288477.894+delta_x, 3496772.181+delta_y) #平移
	points = interpolate(points)#插值
#	points = generateMaxSpeed(points,1.5)
	
	if(len(argv) == 3):
		dumpPoints(argv[2],points)
	
	xs = [point.x for point in points]
	ys = [point.y for point in points]
#	yaws = [point.yaw for point in points]

#	plt.plot(xs, ys, 'r-')
#	plt.axis('equal')
#	plt.show()
	
if __name__ == "__main__":
	main(sys.argv)
