from ase.build import *
from ase.calculators.espresso import Espresso

pseudopotentials = { 'Mo': 'Mo_ONCV_PBE-1.0.oncvpsp.upf', 'S': 's_pbe_v1.4.uspp.F.UPF' }

# build MoS2 electrode

# prepare input file
# include pseudos in dir
inCONTROL = { 'calculation': 'vc-relax', 'outdir': './tmp', 'forc_conv_thr': 0.001 }
inSYSTEM = { 'ecutrho' , 'ecutwfc', 'ibrav', 'celldm(1)', 'nat': 3, 'ntyp': 2, 'tot_charge': 0 } # tot_charge will change
inELECTRONS = { 'conv_thr': 5e-9 }
inIONS = { 'ion_dynamics': 'bfgs' }
inCELL = { 'cell_dynamics': 'bfgs', 'cell_dofree' = '2Dxy' }

infile = {}

# run relax calculation
relax = Espresso()

# run pw calculation
pw = Espresso()
read_espresso_out(_PW_TOTEN_) # read output total energy; returns slice -- use str_to_value() method

'''minimization for dq'''
# build electrode
# perform relax
# add hydrogen
# take total E from output
# determine H2 energy

# perform minimization with qe
# perform minimization with environ
