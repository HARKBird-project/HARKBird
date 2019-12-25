import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.path import Path as MatPath
import pandas as pd

import os
import sys
import signal
import argparse
import subprocess

import Tool


# Class for annotation
class Viewer(object):
    # Constructor
    def __init__(self, ax, fig, LocalizedDir, ResultDir, Result, IsAnnotation):

        # Initialization
        self.ax = ax
        self.fig = fig
        self.PID = None
        self.LocalizedDir = LocalizedDir
        self.ResultDir = ResultDir
        self.Result = Result

        self.IsActive = False
        self.SetLine()
        self.ClearLine()

        # Set signals
        self.ax.figure.canvas.mpl_connect("pick_event", self.OnPick)

        if IsAnnotation:
            self.ax.figure.canvas.mpl_connect("key_press_event", self.Pressed)
            self.line.figure.canvas.mpl_connect("button_press_event", self.OnClick)
            self.line.figure.canvas.mpl_connect("motion_notify_event", self.OnMotion)

    # Set line
    def SetLine(self):
        self.line, = self.ax.plot([], [], "k--", lw=2)

    # Clear line
    def ClearLine(self):
        self.xs = []
        self.ys = []
        self.DrawLine(self.xs, self.ys)

    # Draw line
    def DrawLine(self, xs, ys):
        self.line.set_data(xs, ys)
        self.line.figure.canvas.draw()

    # Mouse clicked
    def OnClick(self, event):
        if (event.inaxes != self.line.axes) or (not self.IsActive):
            return 0

        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.DrawLine(self.xs, self.ys)

    # Mouse moved
    def OnMotion(self, event):
        if (event.inaxes != self.line.axes) or (not (self.xs or self.ys)) or (not self.IsActive):
            return 0

        self.DrawLine(self.xs + [event.xdata, self.xs[0]], self.ys + [event.ydata, self.ys[0]])

    # Key pressed
    def Pressed(self, event):
        sys.stdout.flush()
        if (event.key == "x") and self.xs and self.ys and self.IsActive:
            v = [(x, y) for (x, y) in zip(self.xs, self.ys)]
            v.append((self.xs[0], self.ys[0]))
            Path = MatPath(v)
            self.Annotation(Path)

            self.SetLine()
            self.ClearLine()

        if event.key == "a":
            self.ClearLine()

        if event.key == "z":
            self.IsActive = not self.IsActive

    # Plot clicked
    def OnPick(self, event):
        if (not len(event.ind)) or self.IsActive:
            return 0

        # Get clicked point
        i = event.ind[0]
        Coord = event.artist.get_offsets()
        Point = Coord[i]

        # Search result
        row = self.Result.loc[(self.Result["x0"] == Point[0]) & (self.Result["x1"] == Point[1])]
        if len(row) > 1:
            print("There are same points")

        FolderName = row["folder_names"].values[0]
        FileNumber = str(row["file_numbers"].values[0])

        if (FolderName == "None") or (FileNumber == "None"):
            print("Cannot play birdsong or show spectrogram")
            return 1

        print("Folder name = " + FolderName)
        print("File name = " + "sep_" + FileNumber)

        # Play birdsong and show spectrogram
        self.PlayBirdsong(FolderName, FileNumber)
        self.ShowSpectrogram(FolderName, FileNumber)

    # Play birdsong
    def PlayBirdsong(self, FolderName, FileNumber):
        if self.PID is not None:
            try:
                os.kill(self.PID, signal.SIGTERM)
            except:
                pass

        if self.LocalizedDir is not None:
            Cmd = ["sox", "-q", self.LocalizedDir + FolderName + "/sep_" + FileNumber + ".wav"]
            if os.name == "posix":
                Cmd += ["-d"]
            elif os.name == "nt":
                Cmd += ["-t", "waveaudio"]
            Process = subprocess.Popen(Cmd)
            self.PID = Process.pid

    # Show spectrogram
    def ShowSpectrogram(self, FolderName, FileNumber):
        Image = mpimg.imread(self.ResultDir + "dataset/" + FolderName + "/sep_" + FileNumber + ".png")

        plt.ion()
        plt.figure(1, figsize=(6, 3))
        plt.figure(1).canvas.set_window_title("Folder name = " + FolderName + " : " + "File name = sep_" + FileNumber)
        plt.imshow(Image, aspect="auto", interpolation="bilinear", cmap="jet")
        plt.xticks([], [])
        plt.xlabel("Time")
        plt.yticks([0, 15, 31, 47, 63], ["8000", "6000", "4000", "2000", "0"])
        plt.ylabel("Frequency")
        plt.show()

    # Annotation
    def Annotation(self, Path):
        Label = input("Please input label> ")
        if not Label:
            self.ClearLine()
            return 0

        Index = Path.contains_points(self.Result[["x0", "x1"]])
        for i in range(len(self.Result)):
            if Index[i]:
                self.Result.ix[i, "labels"] = Label

        # Clear figure
        self.fig.clf()

        # Get label names
        LabelNames = Tool.GetLabelNames(self.Result)

        # Get color sequence
        Colors = Tool.MakeColors(LabelNames)

        # Make scatter plot
        self.ax = MakeScatter(self.fig, self.Result, LabelNames, Colors)
        self.ax.legend()

        self.ax.figure.canvas.draw()


# Make scatter plot
def MakeScatter(fig, Result, LabelNames, Colors):
    ax = fig.add_subplot(111)

    # Set axis labels
    ax.set_xlabel("1st dimension")
    ax.set_ylabel("2nd dimension")

    for l in LabelNames:
        ax.scatter(Result[Result["labels"] == l].ix[:, "x0"],
                   Result[Result["labels"] == l].ix[:, "x1"],
                   marker="o",
                   label=l,
                   color=Colors[l],
                   picker=0.5,
                   s=10
                   )

    return ax


# Plot result of deep learning
def PlotResult(Path, Suffix=None, Size=(8, 8), DPI=300, IsViewer=False, IsAnnotation=False, LocalizedDir=None):
    if not IsViewer:
        # Show off
        plt.ioff()

    # Load result data
    if Suffix is not None:
        Result = pd.read_csv(Path + "result/result_" + Suffix + ".csv")
    else:
        Result = pd.read_csv(Path + "result/result.csv")
        Result["labels"] = "None"  # Dummy label

    # Get label names
    LabelNames = Tool.GetLabelNames(Result)

    # Get color sequence
    Colors = Tool.MakeColors(LabelNames)

    # Make figure
    fig = plt.figure(0, figsize=Size)
    if IsViewer:
        fig.canvas.set_window_title("Result")

    # Check dimension of result
    if ("x1" in Result.columns) and ("x2" not in Result.columns):
        ax = MakeScatter(fig, Result, LabelNames, Colors)
    else:
        print("Cannot plot result")
        return 1

    # Make legend
    if Suffix is not None:
        ax.legend()

    # Activate viewer and annotation
    if IsViewer:
        CB = Viewer(ax, fig, LocalizedDir, ResultDir, Result, IsAnnotation)
        plt.show()
        plt.close()

        if IsAnnotation:
            # Save and plot annotated result
            Result.to_csv(ResultDir + "result/result_annotated.csv", index=False)
            PlotResult(ResultDir, Suffix="annotated")

        return 0

    # Save plot as EPS image
    if Suffix is not None:
        FileName = "result_" + Suffix + ".eps"
    else:
        FileName = "result.eps"

#    plt.savefig(Path + "result/" + FileName, format="eps", dpi=DPI)
    tmp = Path.rsplit('/',3)
    plt.savefig(tmp[0] + "/result_eps/" + tmp[-2], format="eps", dpi=DPI)
    plt.close()

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show result and annotation")
    parser.add_argument("-rd", "--ResultDir", required=True, type=str, help="Result directory")
    parser.add_argument("-s", "--Suffix", type=str, help="Suffix")
    parser.add_argument("-a", "--Annotation", action="store_true", default=False, help="Annotation")
    args = parser.parse_args()

    Annotation = args.Annotation

    # Check result directory
    ResultDir = args.ResultDir
    if not os.path.isdir(ResultDir):
        print("Invalid result directory")
        sys.exit()

    if ResultDir[-1] != "/":
        ResultDir += "/"

    # Load localized directory
    LocalizedDir = Tool.LoadLocalizedDir(ResultDir)

    # Check suffix
    Suffix = args.Suffix
    if Suffix is not None:
        if not os.path.isfile(ResultDir + "result/result_" + Suffix + ".csv"):
            print("Invalid suffix")
            sys.exit()

    else:
        Suffix = None

    # Plot result and annotation
    PlotResult(ResultDir, Suffix, IsViewer=True, IsAnnotation=Annotation, LocalizedDir=LocalizedDir)
