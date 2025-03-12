import sys
import pdb

valid = ["H","C", 'N', 'O', "S", "P", "F", "Cl", 'Br', "I", "CL", "BR"] #Handle case? BR/CL 


def check_valid(path):
    try:
        with open(path, 'r') as file:
            contents = file.readlines()
    except FileNotFoundError:
        print("File not found:", path)
    except Exception as e:
        print("An error occurred:", str(e))
    
    mols = []
    for line in contents: 
        if "ATOM" in line or "ATM" in line: 
            line = line[::-1].strip()
            idx = line.find(" ")
            atom = line[:idx][::-1]
            if atom not in valid and atom not in mols: 
                mols.append(atom)
    return (not mols, mols)

def main():
    # Check if the user provided the file path as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python3 your_program.py <file_path>")
        return

    # Get the file path from the command-line arguments
    file_path = sys.argv[1]
    check_valid(file_path)
    # Now you can use the file_path variable to read the file or perform any other operations
    # Example: Reading the contents of the file
    
if __name__ == "__main__":
    print(main())
