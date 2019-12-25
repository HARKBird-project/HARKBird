import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
import scipy as sp
import pandas as pd
import json
from scipy import stats
from PIL import Image

import mic_param


FR= mic_param.FR
L=mic_param.L
W=mic_param.W
W_x=mic_param.W_x
W_y=mic_param.W_y
RANGE= mic_param.RANGE
DIV=mic_param.DIV
center= mic_param.center
positions=mic_param.plot_positions
filename=mic_param.MAPFILE
importmap = mic_param.Import_MAP
SaveDir = mic_param.SaveDir


# Get label names
def GetLabelNames(Result):
    LabelNames = Result["species"].drop_duplicates()
    LabelNames.sort_values(inplace=True)
    LabelNames.reset_index(drop=True, inplace=True)
    return list(LabelNames)

def myHist(array):
    xx, yy = array[0], array[1]
    hist = np.zeros((bin_num, bin_num))

    for x, y in zip(xx, yy):
        if np.abs(x) <= W_x/2 and np.abs(y) <= W_y:
            x = int((bin_num * (x + W_x/2)) // W_x)
            y = int((bin_num * (y + W_y/2)) // W_y)
            hist[x][y] += 1.0

    return hist


plt.figure(figsize=(10, 10))
if(importmap == True):
	img = Image.open(filename)
	plt.imshow(img,extent=[center[0]-W_x/2, center[0]+W_x/2, center[1]-W_y/2, center[1]+W_y/2],alpha=0.7)

r_t = pd.read_table(SaveDir + '/crosspoint_annotated.txt')
r_t = r_t.sort_values(['mic1'])
r_t = r_t.sort_values(['mic2'])
Ln = GetLabelNames(r_t)
Ln.sort()
print Ln
loc_1, loc_2= list(r_t['mic1'].values) , list(r_t['mic2'].values)
loc_set = list(set(zip(loc_1,loc_2)))
loc_set = sorted(sorted(loc_set, key=lambda x: x[0]), key=lambda x: x[1])
print loc_set

plot_data = []
for i,j in loc_set:
	plot_data.append(r_t[ (r_t['mic1'] == i) & (r_t['mic2'] == j) ] )

dic_label = {}

col_file = open(SaveDir +'/2d_set/select_color.json')
col_select = json.load(col_file)


x = []
y = []
for i in plot_data:
	i = i.sort_values(['frame'])
	x_tmp,y_tmp =list(i['x1']), list(i['x2'])
	print list(i['species'])[0]
	if list(i['species'])[0] in dic_label.keys():
		dic_label[list(i['species'])[0]][str(len(dic_label[list(i['species'])[0]]))] =[x_tmp[len(x_tmp)/2],y_tmp[len(y_tmp)/2]]
	else:
		dic_label[list(i['species'])[0]] = {"0":[x_tmp[len(x_tmp)/2],y_tmp[len(y_tmp)/2]]}
	x.append(x_tmp[len(x_tmp)/2])
	y.append(y_tmp[len(y_tmp)/2])
print dic_label
#	print i
#	print x,y

hist_3d = []

colors = cm.gist_rainbow(np.arange(0, len(Ln), 1./len(Ln)))
for idx, (key, pos_dic) in enumerate(dic_label.items()):
	if key != "None":
		xx, yy = [v[0] for v in pos_dic.values()] , [v[1] for v in pos_dic.values()]
		hist_3d.append([xx,yy])
		if key not in col_select:
			plt.scatter(xx,yy, s = 50, alpha = 0.5,label = key, color = colors[idx])
		else:
			plt.scatter(xx,yy, s = 50, alpha = 0.5,label = key, color = col_select[key])
plt.scatter(positions[0][0],positions[0][1],facecolors='none',edgecolor='cyan',s = 50,label='Mic0',marker='^')
plt.scatter(positions[1][0],positions[1][1],facecolors='none',edgecolor='orange',s = 50,label='Mic1',marker='^')



plt.xlabel('x [m]',fontsize=18)
plt.ylabel('y [m]',fontsize=18)
plt.xlim(-W_x/2, W_x/2)
plt.ylim(-W_y/2, W_y/2)
plt.legend(fontsize=18)
plt.tick_params(labelsize=18)
plt.subplots_adjust(left=0.1,bottom=0.1)

plt.savefig(SaveDir + "/2d_mapping_annotated.pdf")
plt.show()

'''
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
bin_num = 16

temp_btm = []
xpos = np.arange(-W_x/2,W_x/2, W_x/bin_num)
rLn = Ln[1:]
rcl = colors[1:]
hist_sum = np.zeros((bin_num, bin_num))
for idx, xy in enumerate(hist_3d):
	hist_sum += myHist(xy)

pos_x, pos_y = np.meshgrid(np.linspace(-W_x/2,W_x/2,128), np.linspace(-W_y/2,W_y/2,128))
#print pos_x,pos_y
zpos = np.full((128,128),0)
ax.plot_surface(pos_x,pos_y,zpos, rstride=1, cstride=1, facecolors=plt.imread("img2(1).jpg")[::-1, :, :]/255., shade=False,alpha=0.1,EdgeColors="none")

for idx, xy in enumerate(hist_3d):
	#x, y = xy
	#hist, xedges, yedges = np.histogram2d(x, y, bins=bin_num, range=[[center[0]-W/2, center[0]+W/2], [center[1]-W/2, center[1]+W/2]])
	hist = myHist(xy)
	#print(hist)
	# Construct arrays for the anchor positions of the 16 bars.
	# Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
	# ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
	# with indexing='ij'.
	"""
	if idx == 0:
		temp_btm.append(np.zeros(len(xpos)))
		temp_btm.append(hist)
	else:
		temp_btm.append(hist)
	for i, h in enumerate(hist):
		ax.bar(xpos[::-1], h, color=colors[idx+1],zs = xpos[i] ,bottom = temp_btm[idx][i],zdir='y',width=W / bin_num -10)
	"""
	print(hist_sum)
	for i in range(len(xpos)):
		for j in range(len(xpos)):
			if hist[i][j] != 0.0:
				ax.bar3d(xpos[i], xpos[j], hist_sum[i][j]-hist[i][j], W_x/bin_num/2.75, W_y/bin_num/2.75, hist_sum[i][j], shade=True, color=rcl[idx])

	hist_sum -= hist
	print(hist_sum)
#ax.imshow(Image.open("black.jpg"),extent=[center[0]-W/2, center[0]+W/2, center[1]-W/2, center[1]+W/2],alpha=0.3)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("frequency")
plt.savefig(SaveDir + "/2d_mapping_hist.pdf")
plt.show()
'''
