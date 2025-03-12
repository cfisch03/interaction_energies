import json
import numpy as np
import matplotlib.pyplot as plt

path = "./testy_drug/res_energies.json"
with open(path, "r") as f: 
    data = json.load(f)


fig2, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2) # two axes on figure

vdw ={}
ele = {} 

# creating the dataset
r1 = list(ele.keys())
v1 = [float(i) for i in ele.values()]
r2 = list(vdw.keys())
v2 = [float(i) for i in vdw.values()]
color = ['gray','pink', 'cyan', 'purple', 'red', '#8aff33']
altcolor = ['gray', 'pink', 'orange', '#8aff33', 'blue']

ax1.bar(list(data.keys()),[float(i[1]) for i in data.values()], color=color)
ax1.set_xlabel("Residue Name", fontsize = 20)
ax1.set_ylabel("Electrostatic Energy", fontsize=20)
ax1.set_title("Test Drug", fontsize = 20)
ax1.set_ybound(lower = -50, upper = 200)
ax2.bar(list(data.keys()), [float(i[0]) for i in data.values()], color=color)
ax2.set_xlabel("Residue Name", fontsize = 20)
ax2.set_ylabel("VDW Energy", fontsize = 20)
ax2.set_title("Test Drug", fontsize =20)
ax2.set_yscale("symlog")
ax2.set_ybound(lower=0, upper =10000000 )

fig2.tight_layout()
plt.show()

# can continue plotting on the first axis
# creating the bar plot

"""plt.bar(residues, values, color=['gray','pink', 'cyan', 'purple', 'red', '#8aff33'])

plt.xlabel("Residue Name", fontsize = 18)
plt.ylabel("Electrostatic Energy", fontsize =18)
plt.title("Electrostatic Energy of each residue on the p53 mutant Y200C within one solvent shell of the docked effector", fontsize = 20)
plt.show()"""
