#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import os
import glob
from datetime import datetime
import numpy as np

import mic_param
print mic_param.SaveDir
subprocess.check_output(["sox","--norm", mic_param.SaveDir + "/mic1/"+mic_param.wavfiles[0], "-c 1", mic_param.SaveDir+"/temp.wav"])
subprocess.check_output(["ffmpeg", "-y", "-framerate", str(100.0/float(mic_param.PERIOD)), "-i", mic_param.SaveDir + "/png/result_%d.png", mic_param.SaveDir + "/video_tmp.mp4"])
subprocess.check_output(["ffmpeg", "-y", "-i", mic_param.SaveDir + "/video_tmp.mp4", "-i", mic_param.SaveDir + "/temp.wav", "-acodec", "copy", mic_param.SaveDir +"/"+mic_param.wavfiles[0][:-3]+".avi"])

