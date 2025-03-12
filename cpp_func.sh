#!/bin/bash

res=$1
directory_name=$2
func=$3
name=$4
cd "$directory_name"
echo $name 
cpptraj << EOF

set res=$res
set func=$func
set name=$name

parm ./complex_wat.prmtop
trajin ./complex_wat.inpcrd 1 last 1 

autoimage

strip :WAT
strip :Na+
strip :Cl-

pairwise @\$res,\$func out total\$res_\$name.out eout indiv\$res_\$name.out vmapout vmap\$res_\$name.out emapout emap\$res_\$name.out avgout avg\$res_\$name.out pdbout pdb\$res_\$name.out

EOF

