from ase.io import read, write, espresso
from ase.calculators.espresso import Espresso

# for q in potentials: # variable charge
# for n in hydrogens: # variable NH

# read cif
cif = read('./MoS2H.cif')
cell = cif.get_cell()
symbols = cif.get_chemical_symbols()
positions = cif.get_positions()
#print(cell, symbols, positions)

# write qe input
n = 0 # test iteration 0
pwin = espresso.write_espresso_in(f"cif{n}.in", cif) # file argument should be a file object, not a string -- raises exception

'''

control = { 'calculation': 'vc-relax', 'pseudodir': './sssp' }
system = { 'ecutrho' , 'ecutwfc', 'ibrav': 0, 'nat': len(symbols), 'ntyp', 'tot_charge' }
electrons = { 'conv_thr': 5e-9 }
ions = { 'ion_dynamics': 'bfgs' }
cell = { 'cell_dynamics': 'bfgs', 'cell_dofree' = 'all' }

# run relax calculation
relax = Espresso()

# run pw calculation
pw = Espresso()
read_espresso_out(_PW_TOTEN_) # read output total energy; returns slice -- use str_to_value() method

'''

'''minimization for dq'''
# build electrode
# perform relax
# add hydrogen
# take total E from output
# determine H2 energy

# perform minimization with qe
# perform minimization with environ

