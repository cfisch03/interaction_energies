#!/bin/bash

# Get the input number
number=$1
file_name=$2

directory_name="${file_name%.*}"
# Check if the number is even or odd
cd "$directory_name"

if [ $((number % 2)) -eq 0 ]; then

  antechamber -i drug_clean_H.pdb -fi pdb -o drug.mol2 -fo mol2 -c bcc -s 2

else

  antechamber -i drug_clean_H.pdb -fi pdb -o drug.mol2 -fo mol2 -c bcc -s 2 -nc -1 

fi

parmchk2 -i drug.mol2 -f mol2 -o drug.frcmod

tleap -s -f upleap.in > tleap.out
