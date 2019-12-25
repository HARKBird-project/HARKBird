import json
import DLocalization_annotated
import numpy as np
from scipy import signal, interpolate
import matplotlib.pyplot as plt
import re
import mic_param
import wave
import os
import multiprocessing
from itertools import izip_longest

period = mic_param.PERIOD
SaveDir = mic_param.SaveDir
plot_args = []

if not os.path.isdir(SaveDir + "/png"):
	os.mkdir(SaveDir + "/png")

fs1 = open(SaveDir + '/mic1/localized_'+mic_param.wavfiles[0]+'/spectrum.txt','r')
fs2 = open(SaveDir + '/mic2/localized_'+mic_param.wavfiles[1]+'/spectrum.txt','r')
fc = open(SaveDir +'/crosspoint_annotated.txt','w')
fc.write('x1' + "\t" + 'x2' + "\t" + 'frame' + "\t" + 'species'  + "\t" + 'mic1' +  "\t" + 'mic2' + "\n")

fs1 = fs1.read().rstrip().split('\n')
spec1 = [i.split('\t') for i in fs1]
fs2 = fs2.read().rstrip().split('\n')
spec2 = [i.split('\t') for i in fs2]

list_len = len(spec1)


 
f = open(SaveDir + '/mic1/localized_'+mic_param.wavfiles[0]+'/sourceinfo_annotated.json', 'r')
json_dict = json.load(f)
data1 = [[]] * list_len
for i in json_dict[0]:
	j = int( float(i['time']) / (period / 100.0))
	duration = int(float(i['duration']) / (period / 100.0))
	for k in range(duration-1):
		if data1[min([list_len-1,j + k])] == []:
			data1[min([list_len-1,j + k])] = ([[(float(i['azimuth'])),(i['species']),int(i['iid'])]])
		else:
			data1[min([list_len-1,j + k])].append(([(float(i['azimuth'])),(i['species']),int(i['iid'])]))
f.close()
f = open(SaveDir + '/mic2/localized_'+mic_param.wavfiles[1]+'/sourceinfo_annotated.json', 'r')
json_dict = json.load(f)
data2 = [[]] * list_len
for i in json_dict[0]:
	j = int( float(i['time']) / (period / 100.0))
	duration = int(float(i['duration']) / (period / 100.0))
	for k in range(duration-1):
		if data2[min([list_len-1,j + k])] == []:
			data2[min([list_len-1,j + k])] = ([[(float(i['azimuth'])),(i['species']),int(i['iid'])]])
		else:
			data2[min([list_len-1,j + k])].append(([(float(i['azimuth'])),(i['species']),int(i['iid'])]))
f.close()

t = np.linspace(-180,180,72)
ttt = np.linspace(0,720,720)
tt = np.linspace(-180,180,720)
#print data1


for i in range(len(data1)): 
	#print i
#	if(data1[i] == [] or data2[i] == []):
#		data = [data1[i],data2[i]]
#		d_type = 3
#	else:
#		data = [[data1[i]],[data2[i]]]
#		d_type = data[0][0][1]
	sp1 = np.array(map(float,spec1[i]))
	sp1 = interpolate.interp1d(t,sp1,kind="cubic")
	sp1 = sp1(tt)
	sp1max = list(signal.argrelmax(sp1))
#	sp1max = [[sp1max[0][i],i] for i in range(len(sp1max[0])) if(sp1[i] > thresh1)]
	sp1max = [sp * 0.5 - 180 for sp in sp1max]


	sp2 = np.array(map(float,spec2[i]))
	sp2 = interpolate.interp1d(t,sp2,kind="cubic")
	sp2 = sp2(tt)
#	print sp2
	sp2max = list(signal.argrelmax(sp2))
	sp2max = [sp * 0.5 - 180 for sp in sp2max]
#	print sp1max
	sp1max = []
	sp2max = []
	if(data1[i] != [] and data2[i] != []):
		print "Step: " + str(i)
		for k in range(len(data1[i])):
			mid_index = int((round(data1[i][k][0]) + 180) *  2)
			sp_num = np.arange(mid_index -5 , mid_index + 5) % len(sp1)
			peak_sp = (mid_index + np.argmax(sp1[sp_num]) - 5) * 0.5 - 180
			print "Mic1  localized:" + str(data1[i][k][0]) +" interpolated:"+ str(peak_sp)
			sp1max.append(peak_sp)
		for k in range(len(data2[i])):
			mid_index = int((round(data2[i][k][0]) + 180) *  2)
			sp_num = np.arange(mid_index -5 , mid_index + 5) % len(sp2)
			peak_sp = (mid_index + np.argmax(sp2[sp_num]) - 5) * 0.5 - 180
			print "Mic2  localized:" + str(data2[i][k][0]) +" interpolated:"+ str(peak_sp)
			sp2max.append(peak_sp)


#			peak_dir = (mid + np.argmax(sp1[(mid+710) % len(sp1):(mid+10) % len(sp1)]) - 10) * 0.5 - 180
#			sp1max.append(peak_dir)
#		print sp1max
#		for k in range(len(data2[i])):
#			mid = int((round(data2[i][k][0]) + 180) *  2)
#			print mid
#			peak_dir = (mid + np.argmax(sp2[(mid+710) % len(sp2):(mid+10) % len(sp2)]) - 10) * 0.5 - 180
#			sp2max.append(peak_dir)
#		print sp2max"
		#sp1max = [sp1max[0][np.abs(np.asarray(sp1max) - data1[i][k][0]).argmin()] for k in range(len(data1[i]))]
		#sp2max = [sp2max[0][np.abs(np.asarray(sp2max) - data2[i][k][0]).argmin()] for k in range(len(data2[i]))]
		#print "sp1:" + str(data1[i][0]) + "   " + str(sp1max)
#		print "sp2:" + str(i) + ":" + str(data2[i]) + "   " + str(sp2max)
		loc_data1 = [ [ sp1max[c], data1[i][c][1],data1[i][c][2] ] for c in range(len(sp1max))]
		loc_data2 = [ [ sp2max[c], data2[i][c][1],data2[i][c][2] ] for c in range(len(sp2max))]
		#print i
		print loc_data1
		#print data1[i]
		print loc_data2
		#print data2[i]
		tdlist,frame,d_type,loc_data, spec, pos, ls= DLocalization_annotated.Dloc([loc_data1,loc_data2],[sp1,sp2],SaveDir)
#		else:
#			tdlist,frame= DLocalization.Dloc([[],[]],1,[sp1,sp2])
	else:
		tdlist,frame,d_type,loc_data, spec, pos, ls= DLocalization_annotated.Dloc([[],[]],[sp1,sp2],SaveDir)

	#plt.plot(ttt,spp1,color = "red",alpha = 0.5)
	#plt.plot(sp1,color = "blue",alpha = 0.5)
	#plt.ylim(24,32)
	#plt.pause(0.001)
	#plt.clf()
	plot_args.append([spec,pos,ls,tdlist,frame])
	for d in range(len(tdlist)):
		fc.write(str(tdlist[d][0]) + "\t" + str(tdlist[d][1]) + "\t" + str(frame) + "\t" + str(d_type[d]) + "\t" + str(loc_data[d][0]) +  "\t" + str(loc_data[d][1]) + "\n")
fc.close()

#split_plot_args = [plot_args[x:x + len(plot_args)/5] for x in range(0, len(plot_args), len(plot_args)/5)]
#for i in split_plot_args:
	
p = multiprocessing.Pool(12)
print 'Making plot image'
p.map(DLocalization_annotated.plot_func,plot_args)
p.close()
print('End plotting')
