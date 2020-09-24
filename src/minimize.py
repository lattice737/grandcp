import os
import json # read pseudos, ecutwfc, ecutrho
from ase.io import read, write, espresso
from ase import Atoms

#for q in potentials: # variable charge
#for n in hydrogens: # variable hydrogen atoms


'''read cif -- working'''
cif = read('./unitcell.cif') # update to receive input; set to MoS2 sample

# make primitive unit cell -- maybe Atoms or geometry tools
# make 2D supercell -- use ase.build.supercells

'''display unit cell'''
cifstr = cif.get_chemical_formula(mode='reduce')
write(f"{cifstr}.png", cif, format='png', show_unit_cell=2, rotation='90x', scale=35)
os.system(f"open {cifstr}.png")
os.system(f"rm {cifstr}.png")

'''get pseudos & cutoffs -- working'''
sssp = json.load( open('./efficiency.json') )

pseudodict = { atom: sssp[atom]['filename'] for atom in cif.get_chemical_symbols() }
rholist = [ sssp[atom]['rho_cutoff'] for atom in cif.get_chemical_symbols() ]
wfclist = [ sssp[atom]['cutoff'] for atom in cif.get_chemical_symbols() ]
rho = min(rholist)
wfc = min(wfclist)


'''write qe input files -- working'''
relaxinput = {
    'control': { 'calculation': 'vc-relax', 'pseudo_dir': './pseudos/' },
    'system': { 'ecutrho': rho, 'ecutwfc': wfc },
    'electrons': { 'conv_thr': 5.E-3 },
    'ions': { 'ion_dynamics': 'bfgs' },
    'cell': { 'cell_dynamics': 'bfgs', 'cell_dofree': 'all' }
    }

n = 0 # remove when loops scripted
pwin = espresso.write_espresso_in( open(f"cif{n}.in",'w'), cif, relaxinput, pseudopotentials=pseudodict )


'''run vc-relax -- debugging'''
pw = '/Users/nicholas/Desktop/qe/bin/pw.x'
# infile, outfile
#os.system( f"{pw} < cif0.in > cif0.out" ) # exception raised: 'charge is wrong; smearing needed' ??

#etot = espresso.read_espresso_out(open('cif0.out'), index=6) # read total energy; RETURNS OBJECT -- NEED ATTRIBUTE
#print(etot)


'''minimization for dq'''
# build electrode (NH = 0) # in progress
# create input files (NH = 1, 2, 3, 4) # DONE
# perform relax in qe # DONE
# take total energy from output # in progress
# take total H energy # with ASE?
# repeat for various system charge
# repeat with environ

