import os
from shutil import copyfile
from refmac_params_file import write_params
from merge_residues import residue_select_hierarchy_from_pdb
from edstats import convert_txt_to_csv_cc
from edstats import plot_edstats_compare

if __name__ == "__main__":

    # Path to KALRNA reference structures
    ref_path = "/dls/labxchem/data/2017/lb18145-17/processing/reference/"

    # Path to output refinements
    refinement_folder = "/dls/labxchem/data/2017/lb18145-17/processing/analysis/multiple_loop_refinements"

    # Path to input refinements
    data_folder =  "/dls/labxchem/data/2017/lb18145-17/processing/analysis/initial_model_rearrangement"

    # Path to structures
    base_pdb = os.path.join(ref_path, "XX02KALRNA-x0074-ground-state.pdb")
    rearranged_pdb = os.path.join(ref_path,"dimple_rearrange_correct_residues.pdb")
    multiple_loop_pdb = os.path.join(ref_path,"alt_multiple_loop.pdb")

    # Residues involved in loop
    loop_residues =[['A', '24'], ['A', '25'], ['A', '26'], ['A', '27'],
                    ['A', '28'], ['A', '29'], ['A', '30'], ['A', '31'],
                    ['A', '32'], ['A', '33'], ['A', '34'], ['A', '35']]

    # All residues
    res_names = "ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE," \
                "LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL"

    input_pdbs = {base_pdb:"base",
                  rearranged_pdb:"rearranged",
                  multiple_loop_pdb: "multiple"}

    # create output folder if it doesn't exist
    if not os.path.exists(refinement_folder):
        os.mkdir(refinement_folder)

    # list of input folders
    dataset_folders = [folder for folder in os.listdir(data_folder)
                       if os.path.isdir(os.path.join(data_folder,folder))]

    for dataset_folder in dataset_folders:

        dataset_copy_folder = os.path.join(refinement_folder,
                                           dataset_folder)

        if not os.path.exists(dataset_copy_folder):
            os.mkdir(dataset_copy_folder)

        dataset = os.path.basename(dataset_copy_folder)

        # Copying free mtz from input folder to output folder
        free_mtz = os.path.join(data_folder,
                                dataset_folder,
                                "{}.free.mtz".format(dataset))

        free_mtz_dst = os.path.join(dataset_copy_folder,
                                    "{}.free.mtz".format(dataset))

        if not os.path.exists(free_mtz_dst):
            copyfile(free_mtz, free_mtz_dst)

        # For rearranged, base and multiple reference structures
        for pdb, type in input_pdbs.items():

            working_dir = os.path.join(dataset_copy_folder, type)

            refine_pdb = os.path.join(working_dir,"refine.pdb")
            refine_mtz = os.path.join(working_dir,"refine.mtz")
            cc_file = os.path.join(working_dir, "residue_cc.txt")
            cc_csv  = os.path.join(working_dir, "residue_cc.csv")

            # Skip refinement if already complete
            if os.path.exists(refine_pdb) and \
               os.path.exists(refine_mtz) and \
               os.path.exists(cc_file) and \
               os.path.exists(cc_csv):
                print("Complete: {} with {}, Skipping Refinement".format(dataset,type))
                continue

            if not os.path.exists(working_dir):
                os.mkdir(working_dir)

            os.chdir(working_dir)

            # Refienement using quick_refine
            # If multiple loop models, set up restraints for total loop occupancy
            if type=="multiple":
                write_params(path=working_dir, residues=loop_residues, name=type)
                os.system("giant.quick_refine {} {} {}".format(
                    pdb, free_mtz_dst, "multiple.params"))
            else:
                os.system("giant.quick_refine {} {}".format(pdb,free_mtz_dst))

            os.system('giant.score_model input.pdb1={} '
                      'input.mtz1={} selection.res_names={} '
                      'output.out_dir="edstats"'.format(refine_pdb, refine_mtz,res_names))

            loop_hier = residue_select_hierarchy_from_pdb(refine_pdb, loop_residues)

            if os.path.exists(refine_pdb) and os.path.exists(refine_mtz):

                if not os.path.exists(cc_file):
                    os.system("phenix.real_space_correlation {} {}"
                              " detail=residue > {}".format(refine_pdb, refine_mtz,
                                                            cc_file))

                if not os.path.exists(cc_csv):
                    convert_txt_to_csv_cc(input_filename=cc_file,
                                          output_filename=cc_csv,
                                          type=type)

        # Separate for loop for plotting
        for pdb, type in input_pdbs.items():

            working_dir = os.path.join(dataset_copy_folder, type)
            cc_csv  = os.path.join(working_dir, "residue_cc.csv")
            print("Plotting: {} with {}, Skipping Refinement".format(dataset, type))

            plot_edstats_compare(input_pdbs=input_pdbs,
                                 refinement_folder=refinement_folder,
                                 dataset=dataset,
                                 csv_name=os.path.basename(cc_csv))


