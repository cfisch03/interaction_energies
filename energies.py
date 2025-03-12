import os 
import json
import pdb
import numpy as np
import pandas as pd 

def create_dict(direct,res,fgs): 
    create_res_dict(direct,res)
    create_func_dict(direct, res, fgs)
    
def create_func_dict(direct, res, fgs):
    oneForces = []
    f_names = [key for key in fgs]
    r_names = []
    #oneForces [func, res] = [VDW, EELEC] 
    res_to_atoms = map_res_to_atoms()
    path = f"./{direct}/"
    for i, func in enumerate(fgs):
        clean = []
        for j, r in enumerate(res):
            pdbpath = path + "/pdb" + str(res_to_atoms[r]) + f"_{i}.out"  #Deleted res.strip()
            resname = gleanRes(pdbpath)
            if i == 0: r_names.append(resname + str(r).strip())
            epath = path + "/total" + str(res_to_atoms[r]) + f"_{i}.out" #Deleted res.strip()
            energies = gleanEnergies(epath)
            clean.append(energies)
        oneForces.append(clean)
    df = pd.DataFrame(oneForces,columns=r_names,index=f_names)
    df.to_csv(path + "func_energies.csv")

def map_res_to_atoms():
    PATH = "../leapfiles/res.csv"
    df = pd.read_csv(PATH)
    my_dict = df.set_index('OneSolv-Res')['OneSolv-Atoms'].to_dict()
    return my_dict

def create_res_dict(direct,residues):
    oneForces = {}
    #oneForces['mol'] = {"res" : ['VDW', 'EELEC']}
    #pdb.set_trace()
    for res in residues:
        path=f"./{direct}"
        pdbpath = path + "/pdb" + str(res) +".out" #Deleted res.strip()
        resname = gleanRes(pdbpath)
        epath = path + "/total" + str(res) + ".out" #Deleted res.strip()
        energies = gleanEnergies(epath)
        key = resname + str(res).strip()
        oneForces[key] = energies
    with open(f"./{direct}/res_energies.json", "w") as outfile:
        json.dump(oneForces, outfile)

def gleanRes(pdbpath):
    with open(pdbpath) as f:
        for i,line in enumerate(f): 
             if i == 1:
                  resname = (line[17:17 + line[17:].find(' ')])
                  return resname

def gleanEnergies(epath): 
    with open(epath) as f:
        for i, line in enumerate(f):
            if i ==1:
                nline = line.strip()[1:].strip()
                vdw = nline[:nline.find(" ")]
                elc= nline[nline.find(" "):].strip()
                return [vdw,elc]

