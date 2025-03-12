#!/bin/sh
file_name=$1

directory_name="${file_name%.*}"

mkdir "$directory_name"

mv "$file_name" "$directory_name/"

mv vina.pdb "$directory_name/"

mv vina_score.txt "$directory_name/"

cp upleap.in "$directory_name/"

cp cpp_res.sh "$directory_name/"

cp cpp_func.sh "$directory_name/"

cd "$directory_name"

pdb4amber --reduce -i vina.pdb -o drug.pdb

obabel drug.pdb -O drug_H.pdb -h

