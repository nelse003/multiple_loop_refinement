import os

def write_params(path, residues, name):

    f = open(os.path.join(path, "{}.params".format(name)), "w+")

    for residue in residues:

        f.write("occupancy groups id 1 chain {} resi     {} alt A\n".format(
            residue[0], residue[1]))
        f.write("occupancy groups id 2 chain {} resi     {} alt B\n".format(
            residue[0], residue[1]))

    f.write("occupancy group alts complete 1 2\n")
    f.write("occupancy refine\n")
    f.write("ncyc 10\n")
    f.write("weight AUTO\n")

    f.close()

