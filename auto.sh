#!/bin/sh
file_name=$1

directory_name="${file_name%.*}"

mkdir "$directory_name"

mv "$file_name" "$directory_name/"

mv vina.pdb "$directory_name/"

mv vina_score.txt "$directory_name/"

cp upleap.in "$directory_name/"

cp cpp.sh "$directory_name/"

cd "$directory_name"

pdb4amber --reduce -i vina.pdb -o drug_H.pdb

antechamber -i drug_H.pdb -fi pdb -o drug.mol2 -fo mol2 -c bcc -s 2

parmchk2 -i drug.mol2 -f mol2 -o drug.frcmod

tleap -s -f upleap.in > tleap.out
