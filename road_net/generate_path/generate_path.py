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

def main():
	paths = loadPaths()
	all_points = []
	last_point = None
	for path in paths:
		path = file_dir+ path
		points = loadPoints(path)
		if(last_point is not None and distance(points[0],last_point)>0.01):
			points.reverse()
		last_point = points[-1]
		points = calPointsInfo(points)
		
		all_points = all_points + points
		
	dumpPoints("output.txt",all_points)

	xs = [point.x for point in all_points]
	ys = [point.y for point in all_points]
	plt.plot(xs,ys,'r')
	plt.show()

if __name__ == "__main__":
	main()
