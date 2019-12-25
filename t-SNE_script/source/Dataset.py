import re
import os
import glob
import subprocess

from PIL import Image
import numpy as np


# Convert wav file for 16k
def ConvertWavFile(FilePath, SavePath):
    cmd = ["sox", FilePath, "-r", "16000", SavePath, "remix", "1"]
    subprocess.call(cmd)


# Make spectrogram
def MakeSpectrogramImage(FilePath, SavePath):
    cmd = ["sox", FilePath, "-n", "spectrogram", "-m", "-r", "-x", "100", "-y", "64", "-o", SavePath]
    subprocess.call(cmd)


# Remove noises from spectrogram
def RemoveNoises(FilePath, Thresh):
    Img = np.asarray(Image.open(FilePath).convert("L"))
    Img.flags.writeable = True
    Img[np.where(Img < Thresh)] = 0
    Image.fromarray(Img).save(FilePath)


# Load image
def LoadImage(FilePath, RNN):
    Img = np.asarray(Image.open(FilePath).convert("L"))
    Img = Img / 255.0  # Shrink values between 0 and 1

    if RNN:
        Img = Img.T
    else:
        Img = np.reshape(Img, (64, 100, 1))  # Shape image to handle in keras

    return Img


# Make dataset from spectrogram images
def MakeDataset(Path, RNN):
    Dataset = []
    FolderNames = []
    FileNumbers = []

    # Load folders' name
    FolderList = glob.glob(Path + "localized_*")

    for f in FolderList:

        # Load images' name
        ImageList = glob.glob(f + "/sep_*")
        for i in ImageList:
            # Load image
            Img = LoadImage(i, RNN=RNN)

            # Add image to dataset
            Dataset.append(Img)
            FolderNames.append(os.path.basename(f))
            FileNumbers.append(re.split(r"[._]", os.path.basename(i))[1])

    # Convert dataset to numpy array
    Dataset = np.array(Dataset)

    return Dataset, FolderNames, FileNumbers


# Make spectrogram images from WAV files
def MakeImages(LocalizedDir, SavePath, Thresh=0):
    if LocalizedDir[-1] != "/":
        LocalizedDir += "/"

    # Make save folder
    if SavePath[-1] != "/":
        SavePath += "/"
    SavePath += "_thresh=" + str(Thresh) + "/"

    if not os.path.exists(SavePath):
        os.mkdir(SavePath)

    # Save path of localized folder
    with open(SavePath + "localized.txt", "w") as f:
        f.write(LocalizedDir + "\n")

    # Load folders' name
    FolderList = [x for x in glob.glob(LocalizedDir + "localized_*")]
    for f in FolderList:

        # Make temporal folder
        if not os.path.exists(SavePath + "tmp"):
            os.mkdir(SavePath + "tmp")

        # Load names of WAV files
        SongList = [x for x in glob.glob(f + "/sep_*.wav")]
        for s in SongList:
            Name, Ext = os.path.splitext(os.path.basename(s))
            TmpSavePath = SavePath + "tmp/" + Name + ".png"

            # Make spectrogram
            MakeSpectrogramImage(s, TmpSavePath)

            # Remove noises from spectrogram
            RemoveNoises(TmpSavePath, Thresh)

        # Rename tmp folder
        os.rename(SavePath + "tmp", SavePath + os.path.basename(f))
    return SavePath
#MakeImages('/home/sumitani/Desktop/amador_2018_sumitani/0504/5/t_1/','/home/sumitani/Desktop/')
