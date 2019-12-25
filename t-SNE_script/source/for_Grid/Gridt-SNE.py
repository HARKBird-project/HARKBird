import os
import json
import shutil
import csv
import numpy as np
from sklearn.manifold import TSNE

import Viewer
import Tool
import Dataset

import pandas as pd

if __name__ == "__main__":
    # Parameters used for grid search
    Parameters = {
        "perplexity": range(5, 50, 20),
        "learning_rate": range(10, 1000, 200),
        "n_iter": range(250, 1000, 200),
        "metric": ["correlation", "cosine", "euclidean"],
        "init": ["random", "pca"],
        "angle": [i / 10.0 for i in range(1, 10, 3)]
    }

    # Directory in which this script is
    ScriptDir = os.path.dirname(os.path.realpath(__file__))

    # Save directory
    SaveDir = ScriptDir.rsplit("/",3)[0]


    if not os.path.isdir(SaveDir + "/t-SNE_Grid"):
        os.mkdir(SaveDir + "/t-SNE_Grid")
    if not os.path.isdir(SaveDir + "/t-SNE_Grid/result"):
        os.mkdir(SaveDir + "/t-SNE_Grid/result")
    if not os.path.isdir(SaveDir + "/t-SNE_Grid/result_eps"):
        os.mkdir(SaveDir + "/t-SNE_Grid/result_eps")

    DatasetDir = SaveDir + "/_thresh=0/"
    CsvDir = SaveDir + "/t-SNE/result/result.csv"
    SaveDir = SaveDir + "/t-SNE_Grid/result"


    # Make dataset
    Data, FolderNames, FileNumbers = Dataset.MakeDataset(DatasetDir, RNN=False)
    Data = np.reshape(Data, (Data.shape[0], Data.shape[1] * Data.shape[2] * Data.shape[3]))
    # Load labels
#    df = pd.read_csv(ScriptDir + "/label_original.csv")
#    df = df.sort_values(by="file_numbers")
#    labels = df["labels"].tolist()

    for p in Tool.DictProduct(Parameters):
        SaveName = ""
        for k, v in p.items():
            SaveName += k + "=" + str(v) + "_"

        SavePath = SaveDir + "/" + SaveName[:-1]
        if not os.path.isdir(SavePath):
            os.mkdir(SavePath)

        if not os.path.isdir(SavePath + "/result"):
            os.mkdir(SavePath + "/result")

        if os.path.isdir(SavePath + "/dataset"):
            shutil.rmtree(SavePath + "/dataset")


        # Copy dataset
        shutil.copytree(DatasetDir, SavePath + "/dataset")

        # Make model
        Model = TSNE(perplexity=p["perplexity"], learning_rate=p["learning_rate"], n_iter=p["n_iter"],
                     metric=p["metric"], init=p["init"], angle=p["angle"], verbose=1)

        # Fitting
        EmbeddedData = Model.fit_transform(Data)

        # Save parameters of model
        with open(SavePath + "/model.json", "w") as f:
            json.dump(Model.get_params(), f, indent=4)

        # Save result
        Result = Tool.MakeResult(EmbeddedData, FolderNames, FileNumbers)
        Result.to_csv(SavePath + "/result/result.csv", index=False)

        # Plot result
        Viewer.PlotResult(SavePath + "/")

        # Save result with label
        Result = pd.read_csv(SavePath + "/result/result.csv")
#        Sorted = Result.sort_values(by="file_numbers")
#        Sorted["labels"] = labels
#        Sorted.to_csv(SavePath + "/result/result_labeled.csv", index=False)
        Viewer.PlotResult(SavePath + "/")
