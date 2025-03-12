import shutil
import sys



def main(path_to,path_from):
    mol2 = [path_to,path_from]
    vs = []
    for path in mol2:
        vector = [0,0,0]
        flag = False
        count = 0
        with open(path,"r") as f: 
            for line in f: 
                fline = line
                if line.startswith("@<TRIPOS>BOND"):
                    break 
                if flag: 
                    count+=1
                    line = line[19:].strip()
                    for i in range(3):
                        idx = line.find(' ')
                        val = line[:idx]
                        vector[i] += float(val)
                        line = line[idx:].strip()
                if line.startswith("@<TRIPOS>ATOM"):
                    flag = True
        for i in range(len(vector)):
            vector[i] /= count
        vs.append(vector)
    avgdiff = []
    for i in range(len(vs[0])):
        avgdiff.append(vs[0][i] - vs[1][i])

    path_new = "trans_drug.mol2"

    with open(path_from, 'r') as file:
        data = file.readlines()


    flag = False
    for idex,line in enumerate(data): 
            vector = [0,0,0]
            if line.startswith("@<TRIPOS>BOND"):
                break 
            if flag: 
                fline = line
                prefix = line[:19]
                postfix = line[46:]
                line = line[19:].strip()
                for i in range(3):
                    neg = 0
                    idx = line.find(' ')
                    val = line[:idx]
                    val = float(val) + avgdiff[i]
                    if val < 0: 
                        neg = 1 
                    vector[i] = val
                    line = line[idx:].strip()
                fix = str(vector[0])[:7 + neg] + "    " + str(vector[1])[:7+ neg] + "    " + str(vector[2])[:7+neg]
                data[idex] = prefix + fix + postfix
        
            if line.startswith("@<TRIPOS>ATOM"):
                flag = True
    with open(path_new, 'w') as file:
        file.writelines(data)
        
if __name__ == "__main__": 
    if len(sys.argv) != 2:
        print("Usage: python3 trans_mol.py <path_to_mol> ")
        sys.exit()
    # Get the file path from the command-line arguments
    file_path_from = sys.argv[1]
    file_path_to = '../leapfiles/site.mol2'
    main(file_path_to,file_path_from)

    

"""
path_to = "/home/lobster/Desktop/Docking_Energies/y220c/22/tleap/ligand.mol2"
path_from = "/home/lobster/Desktop/Docking_Energies/y220c/36.mol2"""
