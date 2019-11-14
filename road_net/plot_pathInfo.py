
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

	#add text
	data = road_file.split('/')
	text,_ = data[-1].split('.')

	plt.plot(points[-1,0],points[-1,1], color) #end point

	if(len(points) == 2):
		plt.plot((points[0,0]+points[1,0])/2, (points[0,1]+points[1,1])/2, color+'.')
		plt.text((points[0,0]+points[1,0])/2, (points[0,1]+points[1,1])/2,text)
	else:
		plt.plot(points[1,0],points[1,1], color+'.')
		plt.text(points[1,0],points[1,1],text)
	
	if(text[-1] == 'c'):
		plt.plot(points[:,0],points[:,1], color+'-.')
	else:
		plt.plot(points[:,0],points[:,1], color)
		
	plt.axis('equal')
	


def listAllDir(path, dir_list):
	lsdir = os.listdir(path)
	dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
	if dirs:
		for i in dirs:
			listAllDir(os.path.join(path, i),dir_list)
	files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
	for f in files:
		dir_list.append(os.path.join(path, f))


def main():
	path = "pathInfo/"
	
	dir_list = []
	listAllDir(path, dir_list)
	
	cnt = 0
	for _file in dir_list:
		data = _file.split('/')
		text,_ = data[-1].split('.');
		if(text[0] == 'R'):
			continue
		color = colorList[cnt%6]
		drawRoad(_file, color)
		cnt = cnt + 1

	#temp
	#drawRoad('j04.txt', 'b*')
	
	plt.savefig('a.pdf',dpi=1200)
	plt.show()



if __name__ == '__main__':
	main()

