from valid_mols import *
from energies import *
import get_elec
import subprocess
import csv
import pdb
from ifg import identify_functional_groups as idfg  
import rdkit   
from rdkit import Chem 
from rdkit.Chem import AllChem
import pandas as pd
import time
from numba import jit 

def preProcessing(smiles,name): 

	try:
		molecule = Chem.MolFromSmiles(smiles)
		fgs = idfg(molecule)
		molecule = Chem.AddHs(molecule)
		AllChem.EmbedMolecule(molecule)
		Chem.MolToPDBFile(molecule, f"./{name}.pdb")
		return fgs  
	except Exception as e: 
		return []
	

def main(path,fgs):
    t0 = time.time()
    directory = path[:path.find(".")]
    flag, mols = check_valid(path)
    if not flag:
        print(f"Invalid molecueles: ", mols)
        sys.exit()
    t1 = time.time()
    vina_script(path)
    dock_time = time.time() - t1
    t1 = time.time()
    leap_prep(path)
    deleteConnect(directory)
    elecs = get_elec.main(os.path.join(directory,'drug_clean_H.pdb'))
    ante_leap(elecs,path)
    ante_time = time.time()-t1
    t1 = time.time()
    res = cpp_script(directory,fgs)
    create_dict(directory,res,fgs)
    cpp_time = time.time() - t1
    print("\n" +"*"*30 + f"\nEnergies Calculated in {time.time()-t0:.2f} seconds" + f"\nDocking: {dock_time:.2f}\nAntechamber + tleap: {ante_time:.2f}\nCpptraj: {cpp_time:.2f}\n" + "*"*30)
   
     
def vina_script(path):
    command = ["./dock.sh",path]
    subprocess.call(command)

def leap_prep(file_name):
    # Define the command to call your Bash script
    command = ["./prep.sh", file_name]
    # Call the command
    subprocess.call(command)

def ante_leap(elecs,fn): 
    command = ["./ant_leap.sh",str(elecs),fn]
    subprocess.call(command)
    
def getAtmIdx(atm,directory): 
    PATH = f"./{directory}/complex.pdb"
    with open(PATH, "r") as f: 
        lines = f.readlines()
    #start_idx = 4361
    #lines = lines[start_idx:]
    for line in lines: 
    	if "UNL" in line and atm in line:
    	    atm_idx = idx_from_line(line)
    	    return atm_idx
@jit
def idx_from_line(line): 
    stripped = line[line.find(" "):].strip()
    atm = stripped[:line.find(" ")]
    return atm
     
def cpp_script(directory,funcs):
    PATH = "../leapfiles/res.csv"
    df = pd.read_csv(PATH)
    res = list(df['OneSolv-Res'])
    for r in res: 
        command =["./cpp_res.sh",str(r),directory]
        subprocess.call(command)
    atoms = list(df['OneSolv-Atoms'])
    start_idx = int(df['Ligand-Atoms'][0])
    for i,fg in enumerate(funcs): 
    	for residue in atoms: 
    	    for atm in funcs[fg]:
    	        atm_idx = getAtmIdx(atm,directory)
    	        command = ['./cpp_func.sh', residue, directory, str(atm_idx), str(i)]
    	        subprocess.call(command)	
    return res

def deleteConnect(directory):
    in_path = "./" + directory + '/drug_H.pdb'
    out_path = "./" + directory + '/drug_clean_H.pdb'
    with open(in_path, 'r') as infile:
        lines = infile.readlines()

    connect_index = None
    for i, line in enumerate(lines):
        if line.startswith("CONECT"):
            connect_index = i
            break

    if connect_index is not None:
        lines = lines[:connect_index]

    with open(out_path, 'w') as outfile:
        outfile.writelines(lines)
  
def extractfgs(fgs,filename):
    clean = {}
    with open("./" + filename, "r") as f: 
        lines = f.readlines()
    start_idx = None
    for i, line in enumerate(lines): 
        if line.startswith("HETATM") or line.startswith("ATOM"):
            start_idx = i 
            break
    if start_idx is not None: 
    	lines = lines[start_idx:]
    for i,func in enumerate(fgs): 
    	cur = []
    	for atm in func[0]: 
    	    key = getAtom(lines[atm],atm)
    	    cur.append(key)
    	clean[func[2]] = cur
    return clean 
    
@jit
def getAtom(line,num):
    num_str = str(num+1)
    idx = line.find(num_str)
    stripped = line[idx+len(num_str):].strip()
    atm = stripped[:stripped.find(" ")]
    return atm

def wrapper(smiles, name): 
    fgs = preProcessing(smiles,name)
    if not fgs: 
    	print("Functional Groups were not identified or there was an issue with converting mol to pdb file")
    	sys.exit(1)
    file_name = f"{name}.pdb"
    fgs = extractfgs(fgs,file_name)
    main(file_name, fgs)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid Number of arguments - usage: python3 auto.py \"smiles\" \"dir_name\"")
        sys.exit()
    # Get the file path from the command-line arguments
    smiles = sys.argv[1]
    name = sys.argv[2]
    fgs = preProcessing(smiles,name)
    if not fgs: 
    	print("Functional Groups were not identified or there was an issue with converting mol to pdb file")
    	sys.exit(1)
    file_name = f"{name}.pdb"
    fgs = extractfgs(fgs,file_name)
    main(file_name, fgs)

