import pandas as pd
from StringIO import StringIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def convert_txt_to_csv_cc(input_filename, output_filename, type):
    files =  open(input_filename,'r').read().split("<id string>")

    df = pd.read_csv(StringIO(files[1]), sep='\s+')

    if type == "multiple":
        b_altloc = df.loc[('A','B')]
        b_altloc['Alt']='B'
        a_altloc = df.loc[('A','A')]
        a_altloc['Alt']='A'
        loop_df = a_altloc.append(b_altloc)
    else:


    loop_df['type'] = type
    loop_df.to_csv(path_or_buf=output_filename)


convert_txt_to_csv_cc("residue_format_test.txt","test.csv","multiple")


# fig = plt.figure()
#
# res_num = [x[1] for x in list(a_altloc.index.values)]
#
# cc_a = a_altloc['CC']
# cc_b = b_altloc['CC']
#
# plt.plot(res_num, cc_a)
# plt.plot(res_num, cc_b)
#
#
#
# plt.savefig("test.png")

# ini_folder = "/dls/labxchem/data/2017/lb18145-17/processing/analysis/initial_model"
#
# print(os.path.join(ini_folder,folder,"dimple.pdb"))
# score_params = score_phil.extract()
# score_params.input.pdb1 = os.path.join(ini_folder,folder,"dimple.pdb")
# score_params.input.mtz1 = os.path.join(ini_folder,folder,"dimple.mtz")
# score_params.output.out_dir = os.path.join(ini_folder,folder,"edstats_on_dimple")
# score_params.selection.res_names= None
# score_model(score_params)
#
# dfs = []

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