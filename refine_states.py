import os
from shutil import copyfile

ref_path = "/dls/labxchem/data/2017/lb18145-17/processing/reference/"
refinement_folder = "/dls/labxchem/data/2017/lb18145-17/processing/analysis/multiple_loop_refinements"
data_folder =  "/dls/labxchem/data/2017/lb18145-17/processing/analysis/initial_model_rearrangement"

base_pdb = os.path.join(ref_path, "XX02KALRNA-x0074-ground-state.pdb")
rearranged_pdb = os.path.join(ref_path,"dimple_rearrange_correct_residues.pdb")
multiple_loop_pdb = os.path.join(ref_path,"multiple_loop.pdb")

input_pdbs = {base_pdb:"base",
              rearranged_pdb:"rearranged",
              multiple_loop_pdb: "multiple"}

if not os.path.exists(refinement_folder):
    os.mkdir(refinement_folder)

dataset_folders = [folder for folder in os.listdir(data_folder)
                   if os.path.isdir(os.path.join(data_folder,folder))]

print(dataset_folders)
exit()

for dataset_folder in dataset_folders:

    dataset_copy_folder = os.path.join(refinement_folder,
                                       dataset_folder)

    if not os.path.exists(dataset_copy_folder):
        os.mkdir(dataset_copy_folder)

    dataset = os.path.basename(dataset_copy_folder)

    free_mtz = os.path.join(data_folder,
                            dataset_folder,
                            "{}.free.mtz".format(dataset))

    free_mtz_dst = os.path.join(dataset_copy_folder,
                                "{}.free.mtz".format(dataset))

    if not os.path.exists(free_mtz_dst):
        copyfile(free_mtz, free_mtz_dst)







