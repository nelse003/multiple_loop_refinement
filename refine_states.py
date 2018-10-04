import os
from shutil import copyfile
from refmac_params_file import write_params

ref_path = "/dls/labxchem/data/2017/lb18145-17/processing/reference/"
refinement_folder = "/dls/labxchem/data/2017/lb18145-17/processing/analysis/multiple_loop_refinements"
data_folder =  "/dls/labxchem/data/2017/lb18145-17/processing/analysis/initial_model_rearrangement"

base_pdb = os.path.join(ref_path, "XX02KALRNA-x0074-ground-state.pdb")
rearranged_pdb = os.path.join(ref_path,"dimple_rearrange_correct_residues.pdb")
multiple_loop_pdb = os.path.join(ref_path,"multiple_loop.pdb")

loop_residues =[['A', '24'], ['A', '25'], ['A', '26'], ['A', '27'],
                ['A', '28'], ['A', '29'], ['A', '30'], ['A', '31'],
                ['A', '32'], ['A', '33'], ['A', '34'], ['A', '35']]

input_pdbs = {base_pdb:"base",
              rearranged_pdb:"rearranged",
              multiple_loop_pdb: "multiple"}

if not os.path.exists(refinement_folder):
    os.mkdir(refinement_folder)

dataset_folders = [folder for folder in os.listdir(data_folder)
                   if os.path.isdir(os.path.join(data_folder,folder))]

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

    for pdb, type in input_pdbs.items():

        working_dir = os.path.join(dataset_copy_folder, type)

        if not os.path.exists(working_dir):
            os.mkdir(working_dir)

        os.chdir(working_dir)
        # if type=="multiple":
        #     write_params(path=working_dir, residues=loop_residues, name=type)
        #     os.system("giant.quick_refine {} {} {}".format(
        #         pdb, free_mtz_dst, "multiple.params"))
        # else:
        #     os.system("giant.quick_refine {} {}".format(pdb,free_mtz_dst))

        refine_pdb = os.path.join(working_dir,"refine.pdb")
        refine_mtz = os.path.join(working_dir,"refine.mtz")

        os.system('giant.score_model input.pdb1={} '
                  'input.mtz1={} res_names=None '
                  'output.out_dir="edstats"'.format(refine_pdb, refine_mtz))

    exit()







