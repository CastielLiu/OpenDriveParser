
# -*-coding=utf-8-*-

import numpy as np
import math
import matplotlib.pyplot as plt
import os


colorList = ['r','g','b','k','y','m','c']

def drawRoad(road_file, color='r-*'):
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
	plt.plot(points[:,0],points[:,1], color)
	plt.axis('equal')
	
	#add text
	data = road_file.split('/')
	text,_ = data[-1].split('.');
	plt.plot(points[1,0],points[1,1], color+'.')
	plt.text(points[1,0],points[1,1],text)
	
	
def main():
	path = "pathInfo/"
	dirs = os.listdir(path)
	cnt = 0
	for _file in dirs:
#		if(_file[0] == 'I'):
#			continue
		color = colorList[cnt%6]
		drawRoad(path+_file, color)
		cnt = cnt + 1
	
	#temp
#	drawRoad('j04.txt', 'b*')
	
	plt.savefig('a.png',dpi=600)
	plt.show()



if __name__ == '__main__':
	main()

