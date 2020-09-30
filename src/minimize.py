import os
import sys
import json # read pseudos, ecutwfc, ecutrho
from ase.io import read, write, espresso
from ase.spacegroup import *
from ase import Atoms

'''read cif -- working'''
cif = read('./unitcell.cif') # update to receive argv input; set to MoS2 sample
cifstr = cif.get_chemical_formula(mode='reduce')

'''simple check for existing files -- working'''
if os.path.exists(cifstr):
    overwrite = input(f"{cifstr} already exists. Overwrite? (y/n): ")
    if overwrite != 'y':
        print('\nGoodbye.')
        quit()
else:
    os.mkdir(cifstr) # make new dir if unit cell dir does not exist
os.chdir(f"./{cifstr}")

# future development: check/make primitive unit cell -- try Atoms or geometry tools

'''get pseudos & cutoffs -- working'''
sssp = json.load( open('../src/efficiency.json') )
pseudodict = { atom: sssp[atom]['filename'] for atom in cif.get_chemical_symbols() }
rho = min([ sssp[atom]['rho_cutoff'] for atom in cif.get_chemical_symbols() ])
wfc = min([ sssp[atom]['cutoff'] for atom in cif.get_chemical_symbols() ])

'''build 2x2 supercell -- working'''
electrode = crystal(cif, size=(2,2,1))
write(f"{cifstr}.png", electrode, format='png', show_unit_cell=2, rotation='5x,30y,90z', scale=35) # electrode image

'''minimize routine -- in progress'''
potentials = [0.0] # 0.0 when testing
hydrogens = [0] # use hydrogens = int() for final script; link to unit cell surface in the future
energies = {}

for i,q in enumerate(potentials): # variable charge
    
    if not os.path.exists(f"Q{i}"): os.mkdir(f"Q{i}") # make new dir if charge dir does not exist
    os.chdir(f"./Q{i}")
    
    for n in hydrogens: # change hydrogens to range(hydrogens+1) in final script

        energies[f"Q{i}"] = {f"H{n}": 0} # {charge: {n-hydrogens: OUTPUT}}

        '''add n-hydrogens to electrode'''
        # this line to add hydrogens -- no changes to cell for now
        if n > 0:
            pseudodict['H'] = sssp['H']['cutoff'] # add hydrogen pseudo
            if int(wfc) > 60: wfc = 60.0
            if int(rho) > 480: rho = 480.0

        '''write qe input files -- working'''
        relaxinput = {
            'control': { 'calculation': 'vc-relax', 'pseudo_dir': '../../src/pseudos/' },
            'system': { 'ecutrho': rho, 'ecutwfc': wfc, 'tot_charge': q, 'degauss': 0.1, 'smearing': 'mv' },
            'electrons': { 'conv_thr': 5.E-3 },
            'ions': { 'ion_dynamics': 'bfgs' },
            'cell': { 'cell_dynamics': 'bfgs', 'cell_dofree': 'all' }
            }

        fin, fout = f"{cifstr}H{n}.in", f"{cifstr}H{n}.out"
        espresso.write_espresso_in( open(fin,'w'), electrode, relaxinput, pseudopotentials=pseudodict )

        '''run vc-relax -- working'''
        pw = '/Users/nicholas/espresso/qe/bin/pw.x' # update to take user input when script complete
        os.system( f"{pw} < {fin} > {fout}" ) # exception raised for H=1: 'charge is wrong; smearing needed' ??
        
        with open(f"{fout}") as f:
            for line in f:
                strlist = line.strip().split()
                if not strlist: continue
                elif strlist[0] == '!':
                    energies[f"Q{i}"][f"H{n}"] = float(strlist[-2])

    os.chdir('../') # back to unit cell directory
    
print(energies) # FOR TESTING

'''minimization for dq'''
# build electrode (NH = 0) # DONE
# create input files (NH = 1, 2, 3, 4) # in progress, adding H to electrode
# perform relax in qe # DONE
# take total energy from output # DONE
# take total H energy # in progress
# repeat for various system charge # in progress
# repeat with environ

