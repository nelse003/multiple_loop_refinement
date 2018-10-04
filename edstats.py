import os
from giant.jiffies.score_model import run as score_model
from giant.jiffies.score_model import master_phil as score_phil
import libtbx.phil
import pandas as pd

ini_folder = "/dls/labxchem/data/2017/lb18145-17/processing/analysis/initial_model"

print(os.path.join(ini_folder,folder,"dimple.pdb"))
score_params = score_phil.extract()
score_params.input.pdb1 = os.path.join(ini_folder,folder,"dimple.pdb")
score_params.input.mtz1 = os.path.join(ini_folder,folder,"dimple.mtz")
score_params.output.out_dir = os.path.join(ini_folder,folder,"edstats_on_dimple")
score_params.selection.res_names= None
score_model(score_params)

dfs = []

# for folder in os.listdir(ini_folder):
#     if os.path.exists(os.path.join(ini_folder,folder,"dimple.pdb")):
#         edstats_csv = os.path.join(ini_folder, folder, "edstats_on_dimple","residue_scores.csv")
#         edstats_df = pd.read_csv(edstats_csv)
#         edstats_df['Dataset'] = folder
#         dfs.append(edstats_df)
#         print(folder)
#         print(edstats_df)
#         print(dfs)


# print("-------------------------------------------")
# compound_edstats = pd.concat(dfs, ignore_index=True)
# print(compound_edstats)
# compound_edstats.to_csv('example.csv')