import os
import sys
import json
import shutil
import argparse
from datetime import datetime as dt

import numpy as np
from sklearn.manifold import TSNE

import Viewer
import Tool
import Dataset

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description="Execute t-SNE")
    parser.add_argument("-sd", "--SaveDir", type=str,default="../", help="Save directory")
    #parser.add_argument("-sn", "--SaveName", type=str, default=dt.now().strftime("%Y-%m-%d_%H-%M") + "/",
                        #help="Save Name")
    parser.add_argument("-sn", "--SaveName", type=str, default="t-SNE/",
                        help="Save Name")
    parser.add_argument("-dd", "--DatasetDir",type=str, default="../", help="Dataset directory")
    parser.add_argument("-p", "--Perplexity", type=float, default=30.0, help="Perplexity")
    parser.add_argument("-lr", "--LearningRate", type=float, default=200.0, help="Learning rate")
    parser.add_argument("-e", "--Epochs", type=int, default=1000, help="Epochs")
    args = parser.parse_args()

    # Make save folders
    SaveDir = args.SaveDir
    SaveName = args.SaveName

    if not os.path.isdir(SaveDir):
        print("Invalid save directory")
        sys.exit()

    if SaveDir[-1] != "/":
        args.SaveDir += "/"
        SaveDir += "/"

    if SaveName[-1] != "/":
        SaveName += "/"

    SavePath = SaveDir + SaveName
    if not os.path.isdir(SavePath):
        os.mkdir(SavePath)

    if not os.path.isdir(SavePath + "result"):
        os.mkdir(SavePath + "result")

    if os.path.isdir(SavePath + "dataset"):
        shutil.rmtree(SavePath + "dataset")


    # Copy dataset
    DatasetDir = args.DatasetDir
    if DatasetDir[-1] != "/":
        args.DatasetDir += "/"
        DatasetDir += "/"

    Dataset_dir = Dataset.MakeImages(DatasetDir,args.SaveDir)

    shutil.copytree(Dataset_dir, SavePath + "dataset")


    # Save parameters
    Parameter = vars(args)
    with open(SavePath + "parameter.json", "w") as f:
        json.dump(Parameter, f, indent=4)


    # Make dataset
    Data, FolderNames, FileNumbers = Dataset.MakeDataset(args.SaveDir+'/_thresh=0/', RNN=False)
    Data = np.reshape(Data, (Data.shape[0], Data.shape[1] * Data.shape[2] * Data.shape[3]))

    # Make model
    Model = TSNE(perplexity=args.Perplexity, learning_rate=args.LearningRate, n_iter=args.Epochs, verbose=2)
    #Model = TSNE(angle=0.1,perplexity=20, learning_rate=10, n_iter=300, metric='cosine',init="random",verbose=2)
    #Model = TSNE(n_components=3,angle=0.1,perplexity=20, learning_rate=10, n_iter=300, metric='cosine',init="random",verbose=2)
    # Fitting
    EmbeddedData = Model.fit_transform(Data)

    # Save parameters of model
    with open(SavePath + "model.json", "w") as f:
        json.dump(Model.get_params(), f, indent=4)

    # Save result
    Result = Tool.MakeResult(EmbeddedData, FolderNames, FileNumbers)
    Result.to_csv(SavePath + "result/result.csv", index=False)

    # Plot result
    Viewer.PlotResult(SavePath)
