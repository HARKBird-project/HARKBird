 # coding:utf-8
import numpy as np
#from pygeocoder import Geocoder
import urllib
import glob
from PIL import Image
import os



# Directory in which this script is
ScriptDir = os.path.dirname(os.path.realpath(__file__))

# Save directory
SaveDir = ScriptDir.rsplit("/",2)[0]
localized_Folder = [
					glob.glob(SaveDir + "/mic1/localized_*.wav")[0].rsplit("/")[-1],
					glob.glob(SaveDir + "/mic2/localized_*.wav")[0].rsplit("/")[-1]]

wavfile_name = [
				localized_Folder[0].rsplit("ed_")[-1],
				localized_Folder[1].rsplit("ed_")[-1]]
print wavfile_name
L = 85.05112878

#position1 = [38.488758,-120.630328]
position1 = [38 + 29/60.0 + 19.35/3600.0,(120 +37 /60.0 + 48.92/3600.0) * -1]
#position2 = [38.488556,-120.630312]
position2 = [38 + 29/60.0 + 18.70/3600.0,(120 +37 /60.0 + 49.13/3600.0) * -1]

# replace xy positions of two microphones
#positions=[[35.211601,137.571974],[35.211655,137.571971]]
positions=[position1,position2]
wavfiles=[wavfile_name[0],wavfile_name[1]]
PERIOD=20

def download_pic(url,filename):
	img = urllib.urlopen(url)
	localfile = open( ScriptDir + str(filename) + ".png" , 'wb')
	localfile.write(img.read())
	img.close()
	localfile.close()

def rotate_Image(degree):
	img = Image.open(ScriptDir + "/img.png")
#	width, height = img.size
#	left = (width - width/2) / 2
#	top = (height - height/2) / 2
#	right = (width + width/2) / 2
#	bottom = (height + height/2) / 2

	new_img = img.rotate(degree)
#	new_img = new_img.crop((left, top, right, bottom))
	new_img.save(ScriptDir + "/img2.png")	

def get_rotation_matrix(rad):
    rot = np.array([[np.cos(rad), -np.sin(rad)],
                  [np.sin(rad), np.cos(rad)]])
    return rot

results=[(positions[0][0]+positions[1][0])/2,(positions[0][1]+positions[1][1])/2]
zoom = 19
rotation = 0
html1 = "https://maps.googleapis.com/maps/api/staticmap?center="
html2 = "&maptype=hybrid&size=512x512&sensor=True&zoom=" + str(zoom) + "&scale=2&key=AIzaSyAioR_Ce5Uk-rS9s_8_NWPcqukNgwCQJvo"

axis = str(results[0]) + "," + str(results[1])
html = html1 + axis + html2
download_pic(html,"/img")
rotate_Image(rotation)


pix_x = 2**(zoom+7)*(results[1]/180 + 1)
pix_y = (2**(zoom+7)/np.pi) * ((-np.arctanh(np.sin(np.pi/180 * results[0]))) + (np.arctanh(np.sin(np.pi/180 * L))))

longitude = 180 *  (((pix_x+256) /  (2**(zoom+7)))  -1)
latitude = (180/ np.pi) * np.arcsin( np.tanh(-np.pi/(2**(zoom+7))*(pix_y+256) + np.arctanh(np.sin(np.pi/180 * L))))

pix_edge_x = np.abs(results[1] - longitude)
pix_edge_y = np.abs(results[0] - latitude)

W_x = 2* pix_edge_x * (6378150 * np.cos(latitude/180. * np.pi) *2. *np.pi / (360.*60.*60.)) / (1./ 60. /60. )
W_y = 2* pix_edge_y * (30.904676 / (1./ 60. /60. ))
RANGE= 8
DIV=1.0
R=300
W=1024
Import_MAP = True
MAPFILE=ScriptDir + "/img2.png"

FR= 10.0
L=15

plot_positions = []

for i in positions:
	#print i
	x = W_x/2 * ((i[1] - results[1]) / pix_edge_x)
	y = W_y/2 * ((i[0] - results[0]) / pix_edge_y)
	point = np.array([x,y])
	#print point
	rot = get_rotation_matrix(rotation*np.pi / 180)
	rotated_point = np.dot(rot,point)
	#print rotated_point
	plot_positions.append([rotated_point[0],rotated_point[1]])
print plot_positions


magnorth= (-13.0+18.0/60.0)
#offset=[0, 0]
offset = [magnorth/360.0*(2.0*np.pi), magnorth/360.0*(2.0*np.pi)]
offset_music = int(round((magnorth / 0.5)))
MICLIST={'1':plot_positions[0],'2':plot_positions[1]}

MICNO= len(MICLIST.keys())

MICNO= len(positions)

center=[0,0]
