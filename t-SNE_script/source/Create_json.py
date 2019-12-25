import pandas as pd
import json as js
import os
import glob
from matplotlib import colors


# Directory in which this script is
ScriptDir = os.path.dirname(os.path.realpath(__file__))

# localized directory
LocalizedDir = ScriptDir.rsplit("/",2)[0]
Folderpath = glob.glob(LocalizedDir + "/localized_*")
print(LocalizedDir)

# get annotated csv file
df_t1 = pd.read_csv(LocalizedDir + '/t-SNE_annotation/result/result_annotated.csv')
df_t1 = df_t1.sort_values(['file_numbers'])

with open('select_color.json') as col_file:
    col_select = js.load(col_file)
    for i,j in col_select.items():
	    col_select[i] = list(colors.to_rgba(j))

print(col_select)

for f in Folderpath:
    Folder_name = f.split("/")[-1]
    df_n = df_t1[df_t1["folder_names"] == Folder_name]
    df_n = df_n["labels"]
    with open(f + '/sourceinfo.json','r') as df_jt1:
        df_jt1 = js.load(df_jt1)
        for i, x in zip(df_jt1[0], df_n):
            i['species'] = x
        df_jt1[1] = col_select
        json_w = open(f +'/sourceinfo_annotated.json','w')
        js.dump(df_jt1, json_w,indent = 4 ,ensure_ascii=False)
