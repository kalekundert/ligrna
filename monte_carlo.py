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

def move_aptamer(construct):
    # Construct.attach()
    # Construct.unattach()
    # Domain.attachment_sites = ...

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

class MonteCarlo:
    # 1. Allow the user to set the parameters of the simulation.
    # 2. Carry out the simulation itself.
    # 3. Filter, rank, and output the best designs.

if __name__ == '__main__':
    # Provide a nice CLI to the design program.
