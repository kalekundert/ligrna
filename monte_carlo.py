#!/usr/bin/env python3

"""\
Monte Carlo RNA design

Usage:
    monte_carlo.py [-c/--cycles=N]

Options:
    -c=N --cycles=N  [default: 10]
        Number of cycles to run simulation.
"""

import sgrna_sensor
import docopt

def score(construct):
    # 1. Fold the constructs with and without constraints.  See show_seqs.py 
    #    for how to call RNAfold.  It might be worth writing wrappers for this.
    # 2. Compute what fraction of the expected base pairs are formed with and 
    #    without constraints.
    #    a. Construct.define_expected_fold()
    #    b. Construct.evaluate_fold()
    # 3. Score the construct based on how well-folded it is with constraints 
    #    and how not-folded it is without them.
    #    a. Maybe consider predicted free energies?
    #    b. Maybe consider several predicted secondary structures?
    pass

def move_aptamer(construct):
    # Construct.attach()
    # Construct.unattach()
    # Domain.attachment_sites = ...
    pass

def mutate_linker(construct):
    # Maybe use Poisson distributions to pick how many residues to mutate and 
    # how many residues to add or remove.
    # Domain.sequence = ...
    # Domain[N] = ...
    # Domain[N:M] = ...
    # Domain.mutate()
    # Domain.insert()
    # Domain.replace()
    # Domain.delete()
    pass

class MonteCarlo:
    # 1. Allow the user to set the parameters of the simulation.
    # 2. Carry out the simulation itself.
    # 3. Filter, rank, and output the best designs.

    def __init__(self, cycles):
        self.cycles = cycles

        self.construct = sgrna_sensor.wt_sgrna()
        self.construct.name = 'MonteCarlo sgRNA'
        
    def run(self):
        print( 'Now running for {} cycles'.format(self.cycles) )
        for i in range(self.cycles):
            print( 'Cycle {}'.format(i+1) )
            

    def show(self):
        self.construct.show()
    
if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    print (args)
    mc = MonteCarlo( int(args['--cycles']) )
    mc.run()
    mc.show()
