import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pandas as pd
from scipy import stats
from PIL import Image

import mic_param


FR= mic_param.FR
L=mic_param.L
W=mic_param.W
RANGE= mic_param.RANGE
DIV=mic_param.DIV
center= mic_param.center
positions=mic_param.plot_positions
filename=mic_param.MAPFILE
importmap = mic_param.Import_MAP

plt.figure(figsize=(10, 10))
if(importmap == True):
	img = Image.open(filename)
	plt.imshow(img,extent=[center[0]-W/2, center[0]+W/2, center[1]-W/2, center[1]+W/2],alpha=0.7)


r_t = pd.read_table('../crosspoint.txt')
r_t = r_t.sort_values(['mic1'])
r_t = r_t.sort_values(['mic2'])
loc_1, loc_2= list(r_t['mic1'].values) , list(r_t['mic2'].values)
loc_set = list(set(zip(loc_1,loc_2)))
loc_set = sorted(sorted(loc_set, key=lambda x: x[0]), key=lambda x: x[1])
print loc_set

plot_data = []
for i,j in loc_set:
	plot_data.append(r_t[ (r_t['mic1'] == i) & (r_t['mic2'] == j) ] )

x = []
y = []
for i in plot_data:
	i = i.sort_values(['frame'])
	x_tmp,y_tmp =list(i['x1']), list(i['x2'])
	x.append(x_tmp[len(x_tmp)/2])
	y.append(y_tmp[len(y_tmp)/2])
#	print i
#	print x,y
plt.scatter(x,y, s = 50, alpha = 0.5,label = 'Sound sources',color='m')

plt.scatter(positions[0][0],positions[0][1],facecolors='none',edgecolor='cyan',s = 50,label='Mic0')
plt.scatter(positions[1][0],positions[1][1],facecolors='none',edgecolor='orange',s = 50,label='Mic1')

plt.xlabel('x [m]',fontsize=24)
plt.ylabel('y [m]',fontsize=24)
plt.xlim(-W/2, W/2)
plt.ylim(-W/2, W/2)
plt.legend(fontsize=24)
plt.tick_params(labelsize=24)
plt.subplots_adjust(left=0.2,bottom=0.2)

plt.savefig("../2d_mapping.pdf")
plt.show()
