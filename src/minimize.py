import os
import json # read pseudos, ecutwfc, ecutrho
from ase.io import read, write, espresso
from ase.spacegroup import *
from ase.atom import Atom # append individual H atoms
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

# future development: check/make primitive unit cell -- try Atoms or geometry tools; maybe crystal.primitive_cellbool

'''get pseudos & cutoffs -- working'''
sssp = json.load( open('../src/efficiency.json') )
pseudodict = { atom: sssp[atom]['filename'] for atom in cif.get_chemical_symbols() }
rho = min([ sssp[atom]['rho_cutoff'] for atom in cif.get_chemical_symbols() ])
wfc = min([ sssp[atom]['cutoff'] for atom in cif.get_chemical_symbols() ])

'''build 2x2 supercell -- working'''
electrode = crystal(cif, size=(2,2,1))
write(f"{cifstr}.png", electrode, format='png', show_unit_cell=2, rotation='5x,30y,90z', scale=35) # electrode image
zmin = min(electrode.get_positions()[:,2]) # max electrode z-coordinate; top surface
zmax = max(electrode.get_positions()[:,2]) # min electrode z-coordinate; bottom surface

'''create hydrogen set -- working'''
hydrogens = [0] # initialize with 0 for enumeration
for o in electrode.get_positions():
    if o[2] == zmin:
        o[2] -= 1
        hydrogens.append(o)
    elif o[2] == zmax:
        o[2] += 1
        hydrogens.append(o)
xmid = [ abs(x - hydrogens[0][0])/2 for x in hydrogens[:,0] if x - hydrogens[0][0] > 0.1 ] # x + xmid = x-midpoint
ymid = [ abs(y - hydrogens[0][1])/2 for y in hydrogens[:,1] if (y - hydrogens[0][1]) > 0.1 ] # y + ymid = y-midpoint
print(xmid, ymid)

'''minimize routine -- working'''
potentials = [0.0] # initialize with 0.0 for enumeration
energies = {}
for i,q in enumerate(potentials): # ith-potential with magnitude q
    
    if not os.path.exists(f"Q{i}"): os.mkdir(f"Q{i}") # make new dir if charge dir does not exist
    os.chdir(f"./Q{i}")
    
    for n,r in enumerate(hydrogens): # n-hydrogens with position r=(x,y,z)

        energies[f"Q{i}"] = {f"H{n}": 0} # {potential: {n-hydrogens: OUTPUT}}

        '''add n-hydrogens to electrode -- working'''
        if n > 0:
            electrode.append(Atom(symbol='H',position=r)) # add hydrogen to electrode
            pseudodict['H'] = sssp['H']['filename'] # add hydrogen pseudo
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

'''hydrogen energy routine -- in progress'''
from ase.build import molecule
H2 = molecule('H2')

# phonon input
phononinput = {
    }

# phonon frequency -- in progress
from ase.phonons import Phonons

# scf calculation
scfinput = {
    'control': { 'calculation': 'scf', 'pseudo_dir': '../../src/pseudos/' }
    'system': { 'ecutrho': 480, 'ecutwfc': 60, 'ibrav': 2, 'celldm(1)': 10, 'nat': 2, 'ntyp': 1 }
    'electrons': { 'conv_thr': 1.E-10 }
    }
espresso.write_espresso_in( open(''), H2, scfinput, pseudopotentials=pseudodict )

'''minimization for dq'''
# build electrode (NH = 0) # DONE
# create input files (NH = 1, 2, 3, 4) # DONE
# perform relax in qe # DONE
# take total energy from output # DONE
# take total H energy # in progress
# repeat for various system charge # in progress
# repeat with environ

