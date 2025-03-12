#!/bin/bash

res=$1
directory_name=$2
cd "$directory_name"


cpptraj << EOF

set res=$res

parm ./complex_wat.prmtop
trajin ./complex_wat.inpcrd 1 last 1 

autoimage

strip :WAT
strip :Na+
strip :Cl-

pairwise :\$res,239 out total\$res.out eout indiv\$res.out vmapout vmap\$res.out emapout emap\$res.out avgout avg\$res.out pdbout pdb\$res.out

EOF

