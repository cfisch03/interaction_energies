#from vina import Vina
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np
import random
import sys
import pdb

"""
lig = rdkit.Chem.MolFromSmiles(sust)
protonated_lig = rdkit.Chem.AddHs(lig)
rdkit.Chem.AllChem.EmbedMolecule(protonated_lig)

prep = MoleculePreparation()
prep.prepare(protonated_lig)
lig_pdbqt = prep.write_pdbqt_string()
"""
def y220c_Dock(path):
    rigid_receptor_path = '../leapfiles/y220c_av.pdbqt'
    ligand_path = path
    v = Vina(sf_name='vina')
    v.set_receptor(rigid_receptor_path)#,flex_recpetor_path)
    v.set_ligand_from_file(ligand_path)
    box_size = [24,40,20]
    #(54.797,71.04,45.391)
    center = [60,65,50]

    #print(center, box_size)
        
    v.compute_vina_maps(center=center, box_size=box_size)
    energy = v.score()
    energy_minimized = v.optimize()

    #print(energy, energy_minimized)
    v.dock(exhaustiveness=32, n_poses=10)
    v.write_poses('vina.pdbqt', n_poses=1, overwrite=True)
    extract_score()

def extract_score():
    best_energy = None
    with open("vina.pdbqt", "r") as f:
        for line in f:
            if line.startswith("REMARK VINA RESULT:"):  # Assuming the line starts with "REMARK VINA RESULT:"
                best_energy = float(line.split()[3])
                break
    with open('vina_score.txt', "w") as f:
        f.write(str(best_energy))


def main():
    # Check if the user provided the file path as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 your_program.py <file_path>")
        return

    # Get the file path from the command-line arguments
    file_path = sys.argv[1]
    y220c_Dock(file_path)
    # Now you can use the file_path variable to read the file or perform any other operations
    # Example: Reading the contents of the file
    
if __name__ == "__main__":
    extract_score()

