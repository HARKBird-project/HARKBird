# -*- coding: utf-8 -*-
# parseTG.py
#import re
#import os, sys
import matplotlib
matplotlib.use('tkAgg')
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import scipy as sp
import math
import pylab
from PIL import Image
import itertools
import collections
#for Canopy users
import matplotlib.animation as animation
  
import random as rnd
import mic_param
  

fname= ""

#----parameters----
#frame rate
FR= mic_param.FR
L=mic_param.L
W=mic_param.W
W_x = mic_param.W_x
W_y = mic_param.W_y 
RANGE= mic_param.RANGE
DIV=mic_param.DIV
center= mic_param.center
offset=mic_param.offset
offset_music=mic_param.offset_music
R=mic_param.R
positions=mic_param.plot_positions
nodecount= len(positions)
filename=mic_param.MAPFILE
importmap = mic_param.Import_MAP
SaveDir = mic_param.SaveDir

fig = plt.figure(figsize=(10, 10))




#additional parmeters for 2d spectrum generation
DIF= 100
cmax= 30.0
cmin= 24.0
miclist= [1, 2]
xspace= np.linspace(center[0]-W_x/2.0, center[0]+W_x/2.0, DIF)
yspace= np.linspace(center[1]+W_y/2.0, center[1]-W_y/2.0, DIF)

frame= 0


def getPolar(x, y):
	return(math.atan2(x, y), (x**2+y**2)**(0.5))


def getCrossPoint(a, b):
	x1s= a[0][0]
	y1s= a[0][1]
	x1e= a[1][0]
	y1e= a[1][1]
	x2s= b[0][0]
	y2s= b[0][1]
	x2e= b[1][0]
	y2e= b[1][1]
	
	A= np.array([[-(y1e-y1s), x1e-x1s], [-(y2e-y2s), x2e-x2s]])
	#print A
	#print 	"det:"+str(np.linalg.det(A))
	if (np.linalg.det(A)!=0):#not parallel
		A_i= np.linalg.inv(A)
		B= np.array([x1e*y1s-y1e*x1s, x2e*y2s-y2e*x2s])
		#print A_i, B
		pt= np.dot(A_i, B)
		return(pt)
	else:
		return(a[0])

def dist(a, b):
	return(np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))

def calcTri(cs):
	"""get the list of j-th DOA with id for each microphone i : cs[i][j][0]->j-th theta (in degree, 0=top=North) of mic i, cs[i][j][1]->j-th id of mic i"""
	# looking for cross point
	#for line_set in list(itertools.product(cs[0], cs[1], cs[2])):
	tcdata=[]
	linesets= []
	species = []
	loc_data = []
	count = 0
	for line_set in list(itertools.product(*cs)):
		if( line_set[0][1] == line_set[1][1] and line_set[0][1] != "None"):
			#picks up one DOA for each mic, and calculates the line from the mic toward the DOA
			tp=[line_set[i][0]*np.pi/180.0 for i in xrange(nodecount)]
			tp_id=[(line_set[i][1]) for i in xrange(nodecount)]
			lines=[None]*nodecount
			for i in xrange(nodecount): 
				deg= (tp[i]+ (np.pi/2.0)+(2.0*np.pi)+offset[i]) % (2.0*np.pi)
				lines[i]= [positions[i], [positions[i][0]+R*np.cos(deg), positions[i][1]+R*np.sin(deg)]]
			
				#Now lines[i][0] represents location of mic i and lines [i][1] represents the point at the DOA and distant from the mic i with R
		#  		print lines
			linesets.append(lines)
			cp={}
			sum_x=0
			sum_y=0
			ok=True
			for pair in itertools.combinations(range(nodecount),2):
				# for each pair of mic i and j
				i=pair[0]
				j=pair[1]
				cp[i,j]=getCrossPoint(lines[i],lines[j])
				sum_x+=cp[i,j][0]
				sum_y+=cp[i,j][1]
				if (lines[i][1][0]-lines[i][0][0])*(cp[i,j][0]-lines[i][0][0])>=0 and (lines[j][1][0]-lines[j][0][0])*(cp[i,j][0]-lines[j][0][0])>=0:
						#checks if the calculated crosspoint is a true crosspoint of the two half lines issuing from two microphones
					pass
				else:
					ok=False
					break
	
					#ax1.plot(cp12[0], cp12[1], marker='+', color='blue')

			if ok==True:
				n=(nodecount*(nodecount-1.0)/2.0)
				cd= [sum_x/n, sum_y/n]
				#Now cd is the center of gravity of nodecountC2 crossing points
				cdd= dist(center, cd)
				if cdd<=W_x and cdd<= W_y :
					#If cd is within the range of the 2D area...
					pairs=list(itertools.combinations(range(nodecount),2))
					for pair in itertools.combinations(pairs,2):
						i=pair[0][0]
						j=pair[0][1]
						k=pair[1][0]
						l=pair[1][1]
						#if dist(cp[i,j],cp[k,l])>=cdd/DIV:
						if dist(cp[i,j],cp[k,l])>RANGE:
							ok=False
							break
					if ok==True:
						#Now cd is finally recognized as the 2D localized position
						"""
						tcdata[t].append([cd[0], cd[1], float(t/100)]+tp_id)
						if out_cross_point!=None:
							xs=sorted(cp.items())
							cp_str=",".join(map(lambda x:",".join(map(str,x[1])) ,xs))
							tp_id_str=",".join(map(str,tp_id))
							fp_cross_point.write(str(t)+","+tp_id_str+","+cp_str+"\n")
						"""
						tcdata.append([cd[0], cd[1]]+tp_id)
						species.append(line_set[0][1])
						loc_data.append([line_set[0][2],line_set[1][2]])
		#returns tcdata: list of localized crossing points, linesets: lines issuing toward the orresponding DOA with the length R
	return (tcdata, linesets, species, loc_data)
	
	
def plotMicarray():
	for (i, m) in enumerate(positions):
		ax.plot(m[0], m[1], "o", markersize=10)
		ax.text(m[0], m[1], str(i), fontsize=15)


def plotLinesets(data):
	for s in data:
		for l in s:
			ax.plot([d[0] for d in l], [d[1] for d in l])

def plotLocalized(data):
	for d in data:
		ax.plot(d[0], d[1], "x", markersize=20)
		ax.text(d[0], d[1], d[2:], fontsize=15)


def plot_func(plot_args):

	if(importmap == True):
		img = Image.open(filename)
		plt.imshow(img,extent=[center[0]-W_x/2, center[0]+W_x/2, center[1]-W_y/2, center[1]+W_y/2],alpha=0.9)
	plt.axis([center[0]-W_x/2, center[0]+W_x/2, center[1]-W_y/2, center[1]+W_y/2])

	plt.imshow(plot_args[0], extent=[center[0]-W_x/2, center[0]+W_x/2, center[1]-W_y/2, center[1]+W_y/2], alpha=0.3, vmax=cmax, vmin=cmin, cmap=plt.cm.jet)

	for (i, m) in enumerate(plot_args[1]):
		plt.plot(m[0], m[1], "o", markersize=5)
		plt.text(m[0], m[1], str(i), fontsize=15)
	for s in plot_args[2]:
		for l in s:
			plt.plot([d[0] for d in l], [d[1] for d in l])
	for d in plot_args[3]:
		plt.plot(d[0], d[1], "x", markersize=20)
		plt.text(d[0], d[1], d[2], fontsize=15)

			#if source_list[0][num]!=[] and source_list[1][num]!=[]:
			#	exportLocalizedWav(1, time_list[0][num], str(source_list[0][num])+"-"+str(source_list[1][num])+".wav", D)
		
	#print td
	#print ls

	#plotMicarray()
	#plotLinesets(ls)
	#plotLocalized(td)

	plt.xlabel('x [m]',fontsize=18)
	plt.ylabel('y [m]',fontsize=18)
	plt.tick_params(labelsize=18)
	plt.subplots_adjust(left=0.1,bottom=0.1)

#	plt.savefig("../pdf/result_" + str(count) +  ".pdf")
	plt.savefig(SaveDir +"/png/result_" + str(plot_args[4]) +  ".png")
	plt.clf()
	if(plot_args[4] % 100 == 0):
		print "result_" + str(plot_args[4]) + '.png was saved.'

def Dloc(currentsources, currentspectrums,Savedir):
	global frame
	#sample data
	#the list of j-th DOA with id for each microphone i : cs[i][j][0]->j-th theta of mic i, cs[i][j][1]->j-th id of mic i
	#currentsources=[[[212, 1]], [[276, 10],[300,8]]]
	#print currentsources

        spectrum2d=np.zeros((len(xspace), len(yspace)))        
        for m in miclist:
		mp= positions[m-1]
		num_ar = np.arange(-offset_music, (len(currentspectrums[m-1]) - offset_music)) % len(currentspectrums[m-1])
		line = currentspectrums[m-1][num_ar]
		#line= [currentspectrums[m-1]]
		spec= [[line[int((((np.pi+np.pi-np.arctan2(-(x-mp[0]), -(y-mp[1])))%(2.0*np.pi))/(2.0*np.pi))*720.0)] for x in xspace] for y in yspace]
		spectrum2d+= np.array(spec)
	spectrum2d= spectrum2d/len(miclist)

	(td, ls,species,Ld) =calcTri(currentsources)

			#if source_list[0][num]!=[] and source_list[1][num]!=[]:
			#	exportLocalizedWav(1, time_list[0][num], str(source_list[0][num])+"-"+str(source_list[1][num])+".wav", D)
		
	#print td
	#print ls

	#plotMicarray()
	#plotLinesets(ls)
	#plotLocalized(td)

	frame+= 1

	return(td,frame,species,Ld,spectrum2d, positions,ls)

