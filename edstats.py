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

    """
    Plot the RSCC scores

    Parameters
    ----------
    input_pdbs
    refinement_folder
    dataset
    csv_name

    Returns
    -------

    """

    fig = plt.figure(figsize=(8,6))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(bottom=True, top=False, left=True, right=False)

    type_col = {"rearranged": '#76cd26',
                "base": '#75bbfd'}

    type_text = {"base": "Initial switch I loop position:\n",
                "rearranged": "Rearranged switch I loop\nposition:\n"}

    for pdb, type in input_pdbs.items():

        df = pd.read_csv(os.path.join(refinement_folder, dataset, type, csv_name))

        if type == "multiple":
            res_num = df['Unnamed: 1'].unique()
            a_altloc = df[df['Alt']=='A']
            b_altloc = df[df['Alt']=='B']
            cc_a = a_altloc['CC']
            mean_occ_a = a_altloc['occ'].mean()
            mean_occ_b = b_altloc['occ'].mean()
            mean_adp_a = a_altloc['ADP'].mean()
            mean_adp_b = b_altloc['ADP'].mean()

            cc_b = b_altloc['CC']

            ax.plot(res_num, cc_a,
                    c='#040273',
                    linestyle='--',
                    linewidth=3,
                     label="Superposed initial\n"
                           "switch I loop position:\n"
                           "mean occupancy:{0:.2f}\n"
                           "mean B-factor:{1:.2f}\n".format(
                         mean_occ_a,mean_adp_a,2))

            ax.plot(res_num, cc_b,
                    color='#0b4008',
                    linestyle='--',
                    linewidth=3,
                     label="Superposed rearranged\n"
                           "switch I loop position:\n"
                           "mean occupancy:{0:.2f}\n"
                           "mean B-factor:{1:.2f}\n".format(
                         mean_occ_b, mean_adp_b))
            continue

        res_num = df['Unnamed: 2'].unique()
        mean_occ = df['occ'].mean()
        mean_adp = df['ADP'].mean()
        cc = df['CC']

        ax.plot(res_num,
                cc,
                linestyle='-',
                linewidth=3,
                color=type_col[type],
                label = "{0}mean occupancy: {1:.2f}\n"
                        "mean B-factor {2:.2f}\n".format(type_text[type],
                                                       mean_occ,
                                                       mean_adp))

    # Shrink current axis by 40%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # Put a legend to the right of the current axis
    handles, labels = plt.gca().get_legend_handles_labels()
    order = [3, 2, 0, 1]

    ax.legend([handles[idx] for idx in order],
              [labels[idx] for idx in order],
              loc='center left',
              frameon=False,
              bbox_to_anchor=(1, 0.5),
              fontsize='x-small',
              handlelength=3)

    plt.title(dataset)
    plt.xlabel('Rac1 Switch I Loop Residues')
    plt.ylabel('Real Space Correlation Coefficient')

    plt.savefig("rscc_{}.png".format(dataset), dpi=300)
    plt.close()


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