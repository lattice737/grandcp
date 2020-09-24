import os
import json # read pseudos, ecutwfc, ecutrho
from ase.io import read, write, espresso
from ase import Atoms

'''read cif -- working'''
cif = read('./unitcell.cif') # update to receive input; set to MoS2 sample

# check/make primitive unit cell -- try Atoms or geometry tools
# make 2D supercell -- use ase.build.supercells

'''display unit cell -- working'''
cifstr = cif.get_chemical_formula(mode='reduce')
write(f"{cifstr}.png", cif, format='png', show_unit_cell=2, rotation='90x', scale=35)
os.system(f"open {cifstr}.png")

potentials = [0.0] # 0.0 when testing
hydrogens = [0] # 0 when testing

for q in potentials: # variable charge
    
    for n in hydrogens: # variable hydrogen atoms

        # this line to add hydrogens -- no changes to cif/cell for now

        '''get pseudos & cutoffs -- working'''
        sssp = json.load( open('./efficiency.json') )
        pseudodict = { atom: sssp[atom]['filename'] for atom in cif.get_chemical_symbols() }
        rho = min([ sssp[atom]['rho_cutoff'] for atom in cif.get_chemical_symbols() ])
        wfc = min([ sssp[atom]['cutoff'] for atom in cif.get_chemical_symbols() ])

        '''write qe input files -- working'''
        relaxinput = {
            'control': { 'calculation': 'vc-relax', 'pseudo_dir': './pseudos/' },
            'system': { 'ecutrho': rho, 'ecutwfc': wfc, 'tot_charge': q },
            'electrons': { 'conv_thr': 5.E-3 },
            'ions': { 'ion_dynamics': 'bfgs' },
            'cell': { 'cell_dynamics': 'bfgs', 'cell_dofree': 'all' }
            }

        espresso.write_espresso_in( open(f"cif{n}.in",'w'), cif, relaxinput, pseudopotentials=pseudodict )

    '''run vc-relax -- debugging'''
    pw = '/Users/nicholas/Desktop/qe/bin/pw.x' # queue to slurm when script complete
    #os.system( f"{pw} < cif{n}.in > cif{n}.out" ) # exception raised for H=1: 'charge is wrong; smearing needed' ??

    '''get output total energy -- ???'''
    output = list( espresso.read_espresso_out('./cif0.out', index=slice(None), results_required=True) )
    print(dir(output[-1].calc))
    #for i in output[-1].calc.results.keys:
    #    print(i)
    
'''remove temporary files'''

'''minimization for dq'''
# build electrode (NH = 0) # in progress
# create input files (NH = 1, 2, 3, 4) # DONE
# perform relax in qe # DONE
# take total energy from output # in progress
# take total H energy # with ASE?
# repeat for various system charge
# repeat with environ

