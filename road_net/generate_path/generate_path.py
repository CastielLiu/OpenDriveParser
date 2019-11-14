# -*-coding=utf-8-*-

import numpy as np
import math
import matplotlib.pyplot as plt
import os
import sys

from map2world import *

def loadPaths():
	paths = []
	with open("paths",'r') as f:
		while True:
			path = f.readline()
			if (len(path) == 0):
				break
			paths.append(path[0:-1] + ".txt")
	return paths

file_dir = "../pathInfo/"

colorList = ['r','g','b','k','y','m','c']

def main():
	paths = loadPaths()
	all_points = []
	last_point = None
	cnt = 0
	for path in paths:
		path = file_dir+ path
		points = loadPoints(path)
		
		if(last_point is not None ):
			dis1 = distance(points[0],last_point)
			dis2 = distance(points[-1],last_point)
			if(dis1 > dis2):
				points.reverse()
		last_point = points[-1]
		###
		points = generateRHO(points) #生成曲率
		
		all_points = all_points + points
		
		xs = [point.x for point in points]
		ys = [point.y for point in points]
		color = colorList[cnt%6]
		plt.plot(xs,ys,color)
		cnt = cnt + 1
	all_points = translationPoints(all_points)
	all_points = interpolate(all_points,0.1)#插值
	dumpPoints("output.txt",all_points)

	
#	xs = [point.x for point in all_points]
#	ys = [point.y for point in all_points]
#	plt.plot(xs,ys,'-o')

#	figure = plt.figure(2)
#	for i in range(2,len(all_points)):
#		xs = [point.x for point in all_points[i-2:i]]
#		ys = [point.y for point in all_points[i-2:i]]
#		plt.plot(xs,ys,'-o')
#		plt.pause(0.001)
		
	plt.show()

if __name__ == "__main__":
	main()
