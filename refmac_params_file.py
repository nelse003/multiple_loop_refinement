import os

loop_residues =[['A', '24'], ['A', '25'], ['A', '26'], ['A', '27'],
                ['A', '28'], ['A', '29'], ['A', '30'], ['A', '31'],
                ['A', '32'], ['A', '33'], ['A', '34'], ['A', '35']]

path = "/dls/labxchem/data/2017/lb18145-17/processing/" \
       "analysis/multiple_loop_refinements/XX02KALRNA-x1604/multiple"

name = "multiple"

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

write_params(path,loop_residues,name)