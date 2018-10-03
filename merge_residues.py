import os
import sys

from giant.structure.utils import transfer_residue_groups_from_other
from iotbx.pdb import hierarchy

sys.path.append('/home/nelse003/PycharmProjects/exhaustive_search')

copy_params = copy_phil.extract()
path = "/home/nelse003/Desktop/"
base_pdb = os.path.join(path, "XX02KALRNA-x0074-ground-state.pdb")
residues_new =[['A','24'],['A','25']]
residues_alter = residue_new
add_pdb = os.path.join(path,"dimple_rearrange.pdb")
copy_params.output.out_dir = copy_params.input.path

set_occ = 0.5

def residue_select_hierarchy_from_pdb(pdb_path, residues_select,
                                      set_occ=None, invert_selection =False):

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
    if invert_selection:
        not_selection_string = "not ({})".format(selection_string)
    new_atoms_sel = sel_cache.selection(selection_string)
    new_atoms_hier = pdb_in.hierarchy.select(new_atoms_sel)

    # Alter occupancy of atoms to be occupied
    if set_occ is not None:
        for chain in new_atoms_hier.only_model.chains():
          for residue_group in chain.residue_groups() :
            for atom_group in residue_group.atom_groups() :
              for atom in atom_group.atoms() :
                  atom.set_occ(set_occ)

    return new_atoms_hier

residue_select_hierarchy_from_pdb(pdb_path, residues_select, set_occ=None)