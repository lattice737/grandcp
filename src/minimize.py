import os
import json # read pseudos, ecutwfc, ecutrho
from ase.io import read, write, espresso
from ase import Atoms

'''read cif -- working'''
cif = read('./unitcell.cif') # update to receive input; set to MoS2 sample

# check/make primitive unit cell -- try Atoms or geometry tools
# make 2D supercell -- use ase.build.supercells

'''display supercell -- displays unit cell'''
#write(f"{cifstr}.png", cif, format='png', show_unit_cell=2, rotation='90x', scale=35)
#os.system(f"open {cifstr}.png")

'''make separate directory'''
cifstr = cif.get_chemical_formula(mode='reduce')
if not os.path.exists(cifstr): os.mkdir(cifstr) # make new dir if unit cell dir does not exist
os.chdir(f"./{cifstr}")

potentials = [0.0] # 0.0 when testing
hydrogens = [0] # use hydrogens = int() for final script; link to unit cell surface in the future

for i,q in enumerate(potentials): # variable charge
    
    if not os.path.exists(f"Q{i}"): os.mkdir(f"Q{i}") # make new dir if charge dir does not exist
    os.chdir(f"./Q{i}")

    for n in hydrogens: # change hydrogens to range(hydrogens+1) in final script

        # this line to add hydrogens -- no changes to cif/cell for now

        '''get pseudos & cutoffs -- working'''
        sssp = json.load( open('../../efficiency.json') )
        pseudodict = { atom: sssp[atom]['filename'] for atom in cif.get_chemical_symbols() }
        rho = min([ sssp[atom]['rho_cutoff'] for atom in cif.get_chemical_symbols() ])
        wfc = min([ sssp[atom]['cutoff'] for atom in cif.get_chemical_symbols() ])

        '''write qe input files -- working'''
        relaxinput = {
            'control': { 'calculation': 'vc-relax', 'pseudo_dir': '../../pseudos/' },
            'system': { 'ecutrho': rho, 'ecutwfc': wfc, 'tot_charge': q },
            'electrons': { 'conv_thr': 5.E-3 },
            'ions': { 'ion_dynamics': 'bfgs' },
            'cell': { 'cell_dynamics': 'bfgs', 'cell_dofree': 'all' }
            }

        if n == 0:
            fin, fout = f"{cifstr}.in", f"{cifstr}.out"
        else:
            fin, fout = f"{cifstr}H{n}.in", f"{cifstr}H{n}.out"
        espresso.write_espresso_in( open(fin,'w'), cif, relaxinput, pseudopotentials=pseudodict )

        '''run vc-relax -- debugging'''
        pw = '/Users/nicholas/Desktop/qe/bin/pw.x' # update to take user input when script complete
        os.system( f"{pw} < {fin} > {fout}" ) # exception raised for H=1: 'charge is wrong; smearing needed' ??
        output = list( espresso.read_espresso_out(fout, index=slice(None), results_required=True) )
        
        #print(dir(output[-1].calc))
        #for i in output[-1].calc.results.keys:
        #    print(i)

    os.chdir('../') # back to unit cell directory
    
'''remove temporary files'''

'''minimization for dq'''
# build electrode (NH = 0) # in progress
# create input files (NH = 1, 2, 3, 4) # DONE
# perform relax in qe # DONE
# take total energy from output # in progress
# take total H energy # with ASE?
# repeat for various system charge
# repeat with environ

