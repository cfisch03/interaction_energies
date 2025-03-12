import sys
import pdb

atm_to_num = {"H": 1 ,
              "C": 6, 
              'N' : 7,
              'O' : 8,
              "S" : 16 ,
              "P" : 15,
              "F" : 9, 
              "Cl" : 17, 
              "CL" : 17,
              'Br': 35, 
              "I" :53} 

def num_elec(atms): 
    return sum(atm_to_num[x] for x in atms)

def get_atms_pdb(path): 
    atms = []
    with open(path, 'r') as f: 
        for line in f: 
            if line.startswith("ATOM") or line.startswith("HETATM"): 
                rev = line[::-1].strip()
                idx = rev.find(" ")
                atm =rev[:idx][::-1]
                atms.append(atm)
    return atms 

def main(path): 
    atms = get_atms_pdb(path)
    num = num_elec(atms)
    return num


if __name__ == '__main__': 

    if len(sys.argv) != 2:
        print("Usage: python3 get_elec.py <file_path>")
        sys.exit(1)

    # Get the file path from the command-line arguments
    file_path = sys.argv[1]
    main(file_path)
    
