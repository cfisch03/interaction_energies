#!/bin/sh

file_name=$1

obabel $file_name -O t.mol2

python3 translate_mol2.py t.mol2

obabel trans_drug.mol2 -O trans.pdbqt

vina --receptor ../leapfiles/y220c_av.pdbqt --ligand trans.pdbqt --center_x 60 --center_y 65 --center_z 50 --size_x 24 --size_y 40 --size_z 20 --out vina.pdbqt --num_modes 1

obabel vina.pdbqt -O vina.pdb

python3 docking.py 

rm vina.pdbqt
rm trans_drug.mol2
rm trans.pdbqt
rm t.mol2

