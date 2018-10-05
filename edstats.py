import os
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
        loop_df = df.iloc[23:35]

    loop_df['type'] = type
    loop_df.to_csv(path_or_buf=output_filename)


def plot_edstats_compare(input_pdbs, refinement_folder, dataset, csv_name):

    fig = plt.figure()
    ax = plt.subplot(111)

    for pdb, type in input_pdbs.items():

        df = pd.read_csv(os.path.join(refinement_folder, dataset, type, csv_name))
        res_num = df['Unnamed: 1'].unique()

        if type == "multiple":
            a_altloc = df[df['Alt']=='A']
            b_altloc = df[df['Alt']=='B']
            cc_a = a_altloc['CC']
            mean_occ_a = a_altloc['occ'].mean()
            mean_occ_b = b_altloc['occ'].mean()
            mean_adp_a = a_altloc['ADP'].mean()
            mean_adp_b = b_altloc['ADP'].mean()

            cc_b = b_altloc['CC']

            ax.plot(res_num, cc_a,
                     label="Multiple: Mean Occ {} Mean B {}".format(
                         mean_occ_a, mean_adp_a))

            ax.plot(res_num, cc_b,
                     label="Multiple: Mean Occ {} Mean B {}".format(
                         mean_occ_b, mean_adp_b))

    # Shrink current axis by 60%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.4, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='x-small')

    plt.savefig("test.png")



        #

        #print(df)









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