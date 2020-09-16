from ase.build import *
from ase.calculators.espresso import Espresso

pseudopotentials = { 'Mo': 'Mo_ONCV_PBE-1.0.oncvpsp.upf', 'S': 's_pbe_v1.4.uspp.F.UPF' }

# build MoS2

infile = {}

# build electrode
calc = Espresso() # run relax
read_espresso_out(_PW_TOTEN_) # read output total energy; returns slice -- use str_to_value() method


'''minimization for dq'''
# build electrode
# perform relax
# add hydrogen
# take total E from output
# determine H2 energy

# perform minimization with qe
# perform minimization with environ
