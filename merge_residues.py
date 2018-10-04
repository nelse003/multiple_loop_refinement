import os
import sys

from giant.structure.utils import transfer_residue_groups_from_other
from iotbx.pdb import hierarchy

def set_all_hier_occ(hier, occ):

    for chain in hier.only_model().chains():
        for residue_group in chain.residue_groups():
            for atom_group in residue_group.atom_groups():
                for atom in atom_group.atoms():
                    atom.set_occ(occ)
    return hier

def set_all_hier_altloc(hier, altloc):

    for chain in hier.only_model().chains():
        for residue_group in chain.residue_groups():
            for atom_group in residue_group.atom_groups():
                atom_group.altloc = altloc

    return hier

def residue_select_hierarchy_from_pdb(pdb_path,
                                      residues_select,
                                      invert_selection=False):

    # read in PDB file from which atoms are to be taken from
    pdb_in = hierarchy.input(file_name=pdb_path)
    sel_cache = pdb_in.hierarchy.atom_selection_cache()

    # produce a hierarchy with atoms to copied
    selection_string_list = []
    chains_new = set()
    for residue_new in residues_select:
        selection_string = "(resid {} and chain {})".format(residue_new[1],
                                                            residue_new[0])
        selection_string_list.append(selection_string)
        chains_new.add(residue_new[0])
    selection_string = "or".join(selection_string_list)

    # Used to select all atoms but residues_select
    if invert_selection:
        selection_string = "not ({})".format(selection_string)

    new_atoms_sel = sel_cache.selection(selection_string)
    new_atoms_hier = pdb_in.hierarchy.select(new_atoms_sel)

    return new_atoms_hier

path = "/dls/labxchem/data/2017/lb18145-17/processing/reference/"
base_pdb = os.path.join(path, "XX02KALRNA-x0074-ground-state.pdb")
rearranged_pdb = os.path.join(path,"dimple_rearrange.pdb")

loop_residues =[['A', '24'], ['A', '25'], ['A', '26'], ['A', '27'],
                ['A', '28'], ['A', '29'], ['A', '30'], ['A', '31'],
                ['A', '32'], ['A', '33'], ['A', '34'], ['A', '35']]

base_loop_hier = residue_select_hierarchy_from_pdb(base_pdb,
                                                   loop_residues)

base_loop_hier = set_all_hier_occ(hier=base_loop_hier, occ=0.5)
base_loop_hier = set_all_hier_altloc(hier=base_loop_hier, altloc='A')

rearranged_loop_hier = residue_select_hierarchy_from_pdb(rearranged_pdb,
                                                         loop_residues)
rearranged_loop_hier = set_all_hier_occ(hier=rearranged_loop_hier, occ=0.5)
rearranged_loop_hier = set_all_hier_altloc(hier=rearranged_loop_hier, altloc='B')

base_hier_no_loop_hier = residue_select_hierarchy_from_pdb(base_pdb,
                                                           loop_residues,
                                                           invert_selection=True)

altloc_loop_changed_hier = transfer_residue_groups_from_other(base_loop_hier,
                                                        base_hier_no_loop_hier,
                                                        in_place=False,
                                                        verbose=False)

multiple_loop_hier = transfer_residue_groups_from_other(rearranged_loop_hier,
                                                        altloc_loop_changed_hier,
                                                        in_place=False,
                                                        verbose=False)

base_pdb_in = hierarchy.input(base_pdb)
f = open(os.path.join(path,"multiple_loop.pdb"), "w+")
f.write(multiple_loop_hier.reset_atom_i_seqs().as_pdb_string(
    crystal_symmetry=base_pdb_in.input.crystal_symmetry()))
f.close()