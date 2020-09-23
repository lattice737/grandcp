import os
import json # read pseudos, ecutwfc, ecutrho
from ase.io import read, write, espresso
from ase.calculators.espresso import Espresso

#for q in potentials: # variable charge
#for n in hydrogens: # variable hydrogen atoms


'''read cif -- working'''
cif = read('./MoS2H.cif') # update to receive input
unit = cif.get_cell() # read unit cell

# this line: to make supercell from unit cell # 2D : 2 x 2 x 0


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
os.system( f"{pw} < cif0.in > cif0.out" ) # exception raised: 'charge is wrong; smearing needed' ??

etot = espresso.read_espresso_out(open('cif0.out'), index=6) # read total energy; RETURNS OBJECT -- NEED ATTRIBUTE
#print(etot)


'''minimization for dq'''
# build electrode
# perform relax
# add hydrogen
# take total E from output
# determine H2 energy

# perform minimization with qe
# perform minimization with environ

