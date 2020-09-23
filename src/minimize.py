import os
from ase.io import read, write, espresso
from ase.calculators.espresso import Espresso

# for q in potentials: # variable charge
# for n in hydrogens: # variable NH

'''read cif'''
cif = read('./MoS2H.cif')
unit = cif.get_cell() # read unit cell

# this line: make supercell # 2D : 2 x 2 x 0

symbols = cif.get_chemical_symbols()
positions = cif.get_positions()
#print(cell, symbols, positions)


'''write qe input'''
relaxinput = {
    'control': { 'calculation': 'vc-relax', 'pseudodir': './pseudos' },
    'system': { 'ecutrho', 'ecutwfc' } # read SSSP_efficiency.json ??
    'electrons': { 'conv_thr': 5e-9 },
    'ions': { 'ion_dynamics': 'bfgs' },
    'cell': { 'cell_dynamics': 'bfgs', 'cell_dofree': 'all' }
    }

n = 0
pwin = espresso.write_espresso_in( open(f"cif{n}.in",'w'), cif, relaxinput, kpts='gamma' ) # does not read 'gamma' properly, need to pass symbols for pseudos

'''
# run relax calculation
relax = Espresso() # read total energy
#etot = ??? # get relax._E_TOT_ ??
'''

'''minimization for dq'''
# build electrode
# perform relax
# add hydrogen
# take total E from output
# determine H2 energy

# perform minimization with qe
# perform minimization with environ

