import pandas as pd 
import pdb
from rdkit import Chem
from rdkit.Chem import AllChem
from auto import wrapper 

path = "/home/lobster/Desktop/previous_mod/DrugDesignThesis/CLEAN/GraphDecomp/SmallDrug.csv"
path_drugs = "./drugs_db.tsv"
#drugs = pd.read_csv(path,error_bad_lines=False,delimiter=';')
drugs = pd.read_csv(path_drugs, sep='\t')

smiles = drugs["Ligand SMILES"]
path_out = "/home/lobster/Desktop/Test_Drugs/Test_Drugs_T/"
i = 55 
for s in smiles[54:]: 
    try:
        wrapper(s, f"cand{i}")
    except: 
        continue
    i +=1 

"""
for i, smile in enumerate(smiles):
    try:
        molecule = Chem.MolFromSmiles(smiles[i])
        molecule = Chem.AddHs(molecule)
        AllChem.EmbedMolecule(molecule)
        mol = f"h{i}.pdb"
        Chem.MolToPDBFile(molecule, path_out + mol)
    except: 
        continue 
"""
