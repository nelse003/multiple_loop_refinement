import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def connectpoints(x, y, x_1, y_1, p1, linestyle="k-"):

    """
    Draw lines between two lists of points

    Parameters
    ----------
    x
    y
    x_1
    y_1
    p1
    linestyle

    Returns
    -------

    """

    x1, x2 = x[p1], x_1[p1]
    y1, y2 = y[p1], y_1[p1]
    plt.plot([x1, x2], [y1, y2], linestyle, lw=0.5)

if __name__ == "__main__":

    # Path to output refinements
    refinement_folder = "/dls/labxchem/data/2017/lb18145-17/processing/" \
                        "analysis/multiple_loop_refinements"
    cc_dfs = []
    cc = []
    for type in ["base", "rearranged", "multiple"]:
        for folder in os.listdir(refinement_folder):
            if os.path.isdir(os.path.join(refinement_folder, folder, type)):

                cc_csv = os.path.join(refinement_folder, folder, type, "residue_cc.csv")
                cc_df = pd.read_csv(cc_csv)
                cc_df['Dataset'] = folder
                cols = list(cc_df.columns.values)

                unnamed_cols = [col for col in cols if "Unnamed" in col]
                unnamed_col_dict = {}
                for col in unnamed_cols:
                    if "THR" in cc_df[col].values:
                        unnamed_col_dict[col] = "Residue"
                    elif "A" in cc_df[col].values:
                        unnamed_col_dict[col] = "Chain"
                    elif 24 in cc_df[col].values:
                        unnamed_col_dict[col] = "resid"

                cc_df = cc_df.rename(columns = unnamed_col_dict)
                cc_dfs.append(cc_df)

    cc_all_df = pd.concat(cc_dfs, ignore_index=True)

    cc_all_df.to_csv("cc_summary.csv")

    multiple_mean_df = cc_all_df.groupby(["Dataset","type","Alt"]).mean()
    base_df = cc_all_df[cc_all_df['type'] == "base"]
    base_df = base_df.groupby("Dataset").mean()

    rearranged_df = cc_all_df[cc_all_df['type'] == "rearranged"]
    rearranged_df = rearranged_df.groupby("Dataset").mean()

    multiple_mean_df['CC_weighted'] = multiple_mean_df['CC'] * multiple_mean_df['occ']

    multiple_cc = multiple_mean_df.groupby(["Dataset","type"]).sum()['CC_weighted']
    multiple_cc = multiple_cc.reset_index(level=1, drop=True)

    cc_diff = base_df['CC'] - rearranged_df['CC']
    cc_diff.to_csv("cc_diff_1.csv")

    #plt.scatter(multiple_cc.index, multiple_cc.values, c='b')
    #plt.scatter(base_df.index, base_df['CC'], c='r')
    #plt.scatter(rearranged_df.index, rearranged_df['CC'], c='g')
    #plt.show()
    #plt.close()

    cc_diff = pd.read_csv("cc_diff.csv")
    cc_diff_ini = cc_diff[cc_diff['Label']=="Initial Switch 1 position"]
    cc_diff_unsure = cc_diff[cc_diff['Label']=="Unsure"]
    cc_diff_rearranged = cc_diff[cc_diff['Label']=="Rearranged Switch 1 position"]

    print(multiple_mean_df)
    multiple_mean_df.to_csv("multiple_mean.csv")

    fig = plt.figure(figsize=(15,6))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.scatter(x=cc_diff_ini['Dataset'],
                y=cc_diff_ini['cc_diff'],
                c=(1.0,0.87,0.37),
                label="Initial switch 1 loop position")

    plt.scatter(x=cc_diff_unsure['Dataset'],
                y=cc_diff_unsure['cc_diff'],
                c=(0.6,0.6,0.6),
                label="Further information required")
    plt.scatter(x=cc_diff_rearranged['Dataset'],
                y=cc_diff_rearranged['cc_diff'],
                c=(1.0,0.5,0.0),
                label="Rearranged switch 1 loop position")

    plt.xticks(rotation=90)
    leg = plt.legend(loc='best', frameon=False, fontsize=16)
    leg.set_title("Crystallographer classification", prop={'size': 18})
    plt.xlabel('Dataset', fontsize=16)
    plt.ylabel('RSCC initial\nswitch I\nloop position\n-\nRSCC rearranged\ninitial switch I\nloop position',
               rotation='horizontal',labelpad=70, fontsize=16)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=14)
    ax.yaxis.set_label_coords(-0.15,0.3)
    plt.savefig("RSCC_XX02KALRNA_difference", bbox_inches = 'tight')
    plt.close()

    multiple_mean_unsure_df = pd.read_csv("multiple_mean_unsure.csv")

    multiple_mean_unsure_df_A = multiple_mean_unsure_df[multiple_mean_unsure_df['Alt']=='A']
    multiple_mean_unsure_df_B = multiple_mean_unsure_df[multiple_mean_unsure_df['Alt']=='B']

    #print(multiple_mean_unsure_df_A)
    #print(multiple_mean_unsure_df_B)

    #multiple_mean_unsure_df_A.plot(x='occ', y='ADP', c='r', kind='scatter')
    #multiple_mean_unsure_df_B.plot(x='occ', y='ADP', c='b', kind='scatter')

    #print(multiple_mean_unsure_df_A['ADP'].values-multiple_mean_unsure_df_B['ADP'].values)

    #plt.hist(multiple_mean_unsure_df_A['ADP'].values-multiple_mean_unsure_df_B['ADP'].values)
    # plt.scatter(multiple_mean_unsure_df_A['occ'].values-multiple_mean_unsure_df_B['occ'].values,
    #             multiple_mean_unsure_df_A['CC'].values-multiple_mean_unsure_df_B['CC'].values,)

    #print(multiple_mean_df.columns.values)
    mean_df = cc_all_df.groupby(["Dataset", "type","Alt"]).mean()
    mean_df = mean_df.reset_index()

    # print(cc_all_df.columns.values)
    # print(mean_df.columns.values)
    # print(mean_df)

    mean_df_A = mean_df[mean_df['Alt']=='A']
    mean_df_B = mean_df[mean_df['Alt']=='B']

    # plt.scatter(x=mean_df_A['ADP'],
    #             y=mean_df_A['CC'])
    #
    # plt.scatter(x=mean_df_B['ADP'],
    #             y=mean_df_B['CC'])

    # A base, B rearrnaged

    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for i in np.arange(len(multiple_mean_unsure_df_A['ADP'])):
        connectpoints(x=np.array(multiple_mean_unsure_df_A['ADP']),
                      y=np.array(multiple_mean_unsure_df_A['CC']),
                      x_1=np.array(multiple_mean_unsure_df_B['ADP']),
                      y_1=np.array(multiple_mean_unsure_df_B['CC']),
                      p1=i,
                      linestyle='k--')

    plt.scatter(x=multiple_mean_unsure_df_A['ADP'],
                y=multiple_mean_unsure_df_A['CC'],
                color=(0.6,0.6,0.6),
                marker='o',
                facecolors='none',
                label="Rearranged switch 1 loop position")

    plt.scatter(x=multiple_mean_unsure_df_B['ADP'],
                y=multiple_mean_unsure_df_B['CC'],
                color=(0.6,0.6,0.6),
                marker='s',
                facecolors='none',
                label="Initial switch 1 loop position")

    ax.axhline(y=0.8,ls='--', color='orange')
    ax.axhline(y=0.7, ls ='--', color='red')
    ax.axhline(y=0.9, ls='--', color ='green')

    plt.ylabel("RSCC")
    plt.xlabel("B factor")
    leg = plt.legend(fontsize=6,
                     loc='lower right',
                     frameon=False)

    leg.set_title(title="Superposed model for datasets\n"
                     "classified as\n"
                     "\"further information required\"",
                  prop={'size': 8})

    plt.savefig("RSCC_B_occ_unsure", bbox_inches = 'tight',dpi=300)

