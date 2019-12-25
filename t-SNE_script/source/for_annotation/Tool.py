import os
import re
import json

import numpy as np
import pandas as pd
from matplotlib import cm as cm


# Load Localized directory
def LoadLocalizedDir(ResultDir):
    Path = ""
    if os.path.isfile(ResultDir + "dataset/localized.txt"):
        f = open(ResultDir + "dataset/localized.txt", "r")
        Path = f.readline().rstrip()
        f.close()

    if not os.path.isdir(Path):
        while not os.path.isdir(Path):
            Path = input("Please input a path of localized directory('None' means 'no localized directory')>")
            if Path == "None":
                return None

        f = open(ResultDir + "dataset/localized.txt", "w")
        f.write(Path + "\n")
        f.close()

    if Path[-1] != "/":
        Path += "/"

    return Path


# Make result dataframe
def MakeResult(EncodedData, FolderNames, FileNumbers):
    Column = ["folder_names", "file_numbers"]
    Result = {}
    Result["folder_names"] = FolderNames
    Result["file_numbers"] = FileNumbers
    for i in range(EncodedData.shape[1]):
        Column.append("x" + str(i))
        Result["x" + str(i)] = EncodedData[:, i]

    Result = pd.DataFrame(Result, columns=Column)

    return Result


# Load parameter
def LoadParameter(ResultDir):
    with open(ResultDir + "parameter.json", "r") as f:
        Parameter = json.load(f)
        return Parameter


# Change backend
def ChangeBackend(Backend):
    os.environ["KERAS_BACKEND"] = Backend


# Switch between CPU and GPU
def SwitchCPUandGPU(GPU, Backend):
    if Backend == "tensorflow":
        import tensorflow as tf
        from keras.backend import tensorflow_backend

        if GPU is None:
            # CPU
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        else:
            # GPU
            config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True, visible_device_list=str(GPU)))
            session = tf.Session(config=config)
            tensorflow_backend.set_session(session)

        return 0

    if Backend == "cntk":
        from cntk.device import cpu, gpu, try_set_default_device

        if GPU is None:
            # CPU
            try_set_default_device(cpu())
        else:
            # GPU
            try_set_default_device(gpu(GPU))

        return 0


# Get parameters of dataset
def GetDatasetParameter(DatasetPath):
    DatasetName = os.path.basename(DatasetPath[:-1])
    DatasetName = DatasetName.split("_")
    Parameter = DatasetName[-1]
    Parameter = re.split(r"[=;]", Parameter)
    DatasetParameter = dict(zip(Parameter[0::2], Parameter[1::2]))

    return DatasetParameter


# Make data for annotation tool in HARKBird
def MakeHARKBirdData(ResultDir, Suffix):
    # Make save folder
    if ResultDir[-1] != "/":
        ResultDir += "/"

    SaveDir = ResultDir + "harkbird/"
    if not os.path.isdir(SaveDir):
        os.mkdir(SaveDir)

    SaveDir += Suffix + "/"
    if not os.path.isdir(SaveDir):
        os.mkdir(SaveDir)

    # Check suffix
    if not os.path.isfile(ResultDir + "result/result_" + Suffix + ".csv"):
        print("Invalid suffix")
        return 1

    # Load data
    Result = pd.read_csv(ResultDir + "result/result_" + Suffix + ".csv")

    # Get folder names
    FolderNames = Result["folder_names"].drop_duplicates()
    FolderNames.reset_index(drop=True, inplace=True)

    # Load Localized directory
    LocalizedDir = LoadLocalizedDir(ResultDir)
    if LocalizedDir is None:
        print("No localized directory")
        return 1

    # Make HARKBird data for each localized folder
    for f in FolderNames:
        Data = []

        # Load sourcelist
        SourceList = pd.read_table(LocalizedDir + f + "/sourcelist.csv", index_col="Sep")

        # Reshape result
        df = Result[Result["folder_names"] == f]
        LabelNames = GetLabelNames(df)
        Colors = MakeColors(LabelNames)
        df["file_numbers"] = df["file_numbers"].astype("int")
        df.set_index("file_numbers", drop=True, inplace=True)
        df.sort_index(inplace=True)

        # Convert result for HARKBird data
        for Sep, Row in SourceList.iterrows():
            Tmp = {"iid": str(Sep), "sid": str(Sep), "time": str(Row["Start time"]),
                   "duration": str(Row["End time"] - Row["Start time"]), "azimuth": str(Row["Start azimuth"]),
                   "species": df.ix[Sep, "labels"]}
            Data.append(Tmp)

        with open(SaveDir + f + ".json", "w") as sf:
            JsonData = [Data, Colors]
            json.dump(JsonData, sf, indent=4)

    return 0


# Make color sequence
def MakeColors(LabelNames):
    print(LabelNames)
    Colors = dict(zip(set(LabelNames), map(tuple, cm.rainbow(np.arange(0, LabelNames.size, 1./LabelNames.size)))))
    return Colors


# Get label names
def GetLabelNames(Result):
    LabelNames = Result["labels"].drop_duplicates()
    LabelNames.sort_values(inplace=True)
    LabelNames.reset_index(drop=True, inplace=True)
    return LabelNames
