import os
import subprocess
import time
import scipy.io.wavfile as wio
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from PySide import QtGui


def ExecuteProcess(Title, Cmd, Wait):
    Cmd = " ".join(Cmd)
    if os.name == "posix":
        Process = subprocess.Popen(["xterm", "-T", Title, "-bg", "black", "-fg", "green", "-e", Cmd + " ; sleep 5"])
    elif os.name == "nt":
        Process = subprocess.Popen(
            ["cmd", "/c", "title " + Title + " & mode con:cols=80 lines=20 & " + Cmd + " & timeout 5"],
            creationflags=subprocess.CREATE_NEW_CONSOLE)
    if Wait:
        Process.wait()

    return Process


def WaitProcess(ProcessList):
    while ProcessList:
        for p in ProcessList:
            Returned = p.poll()

            if Returned is not None:
                ProcessList.remove(p)

        time.sleep(0.5)
        continue


def GetLength(SourceWav):
    Data, SampleRate = sf.read(SourceWav)
    sf.write(SourceWav, Data, SampleRate)
    return eval(subprocess.check_output(["sox", "--i", "-D", SourceWav]))


def MakeFigure():
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot(2, 1, 2)
    ax2 = plt.subplot(2, 1, 1, sharex=ax)

    return fig, ax, ax2


def LoadSourceWav(self, FolderName):
    SourceWav = ""
    if os.path.isfile(FolderName + "sourcewav.txt"):
        f = open(FolderName + "sourcewav.txt", "r")
        SourceWav = f.readline().rstrip()
        f.close()

    if not os.path.isfile(SourceWav):
        (SourceWav, Ext) = QtGui.QFileDialog.getOpenFileName(self, "Choose source wav file", FolderName, filter="*.wav")
        SourceWav = str(SourceWav)
        f = open(FolderName + "sourcewav.txt", "w")
        f.write(SourceWav + "\n")
        f.close()

    if not SourceWav:
        raise
    else:
        return SourceWav


def MakeRemixWav(FolderName, SourceWav):
    RemixWav = FolderName + "remixed.wav"

    if not os.path.isfile(RemixWav):
        Cmd = ["sox", SourceWav, "-b","32", RemixWav, "remix", "1"]
        subprocess.call(Cmd)

    if not os.path.isfile(RemixWav):
        raise
    else:
        return RemixWav


def ShowSpectrogram(ax, Wav, XVisible):
    ax.clear()
    Rate, Data = wio.read(Wav)
    ax.specgram(Data, Fs=Rate, cmap="jet")

    if XVisible:
        ax.set_xlabel("second",fontsize=20)
    else:
        ax.xaxis.set_visible(False)
    ax.set_ylabel("frequency",fontsize=20)
    ax.tick_params(labelsize=20)
    ax.set_ylim([0, 8000])

    ax.figure.canvas.draw_idle()


def ShowMUSIC(ax, FolderName, Length):
    ax.clear()
    Music = np.loadtxt(FolderName + "spectrum.txt").transpose()

    #Add this line
#    Music= list(Music[len(Music)/2:])+list(Music[:len(Music)/2])

    ax.imshow(Music, extent=[0, Length, 180, -180], aspect="auto", interpolation="bilinear", alpha=0.7, cmap="jet")
    ax.tick_params(labelsize=20)
    ax.set_xlabel("second",fontsize=20)
    ax.set_ylabel("azimuth",fontsize=20)
    ax.set_ylim([-200, 200])

    ax.figure.canvas.draw_idle()


def ShowSpecMUSIC(ax, ax2, RemixWav, FolderName, Length):
    ShowSpectrogram(ax2, RemixWav, False)
    ShowMUSIC(ax, FolderName, Length)
