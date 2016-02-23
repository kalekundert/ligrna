#!/usr/bin/env python

from .sequence import *
from .helpers import *

def t7_promoter(source='briner'):
    """
    Return the sequence for the T7 promoter.

    Parameters
    ----------
    source: 'briner', 'igem'
        Specify which T7 sequence to use.  All the sequences are similar, but 
        different sequences may give better or worse transcription.
    """
    if source == 'igem':
        # The "T7 consensus -10 and rest" sequence from IGEM:
        # http://parts.igem.org/Promoters/Catalog/T7
        sequence = 'TAATACGACTCACTATA'

    elif source == 'briner':
        # The T7 sequence used by Briner et al. (2014):
        sequence = 'TATAGTAATAATACGACTCACTATAG'

    else:
        raise ValueError("Unknown T7 sequence: '{}'".format(source))

    return Construct(
            '{} t7'.format(source),
            Domain('t7', sequence))

def manual(*sequences):
    from itertools import cycle

    if len(sequences) == 1:
        colors = 'white',
    else:
        colors = 'magenta', 'red', 'yellow', 'green', 'cyan', 'blue'

    return Construct('manual', [
        Domain('.', seq, style=color)
        for seq, color in zip(sequences, cycle(colors))
    ])

def spacer(name='aavs'):
    """
    Return the specified spacer sequence.

    Parameters
    ----------
    target: 'rfp', 'aavs', 'vegfa'
        The sequence to target.
    """
    if name == 'rfp':
        sequence = 'AACTTTCAGTTTAGCGGTCT'
    elif name == 'gfp':
        sequence = 'CATCTAATTCAACAAGAATT'
    elif name == 'aavs':
        sequence = 'GGGGCCACTAGGGACAGGAT'
    elif name == 'vegfa':
        sequence = 'GGGTGGGGGGAGTTTGCTCC'
    elif name in ('k1', 'klein1'):
        sequence = 'GGGCACGGGCAGCTTGCCCG'
    elif name in ('k2', 'klein2'):
        sequence = 'GTCGCCCTCGAACTTCACCT'
    else:
        raise ValueError("Unknown spacer: '{}'".format(name))

    spacer = Domain('spacer', sequence)
    spacer.style = 'white'

    return Construct(name, spacer)

def repeat(name, length, pattern='UUUCCC'):
    """
    Construct a repeating sequence using the given pattern.

    Oct 31, 2015: After having read some more of the literature, especially 
    Rhiju's EteRNA papers, I've realized that poly-A is a more common 
    "unstructured" linker sequence.

    Parameters
    ----------
    length: int
        Indicate how long the final sequence should be.

    pattern: str
        Provide the basic unit that should be repeated to make the sequence.
    """
    sequence = pattern * (1 + length // len(pattern))
    return Domain(name, sequence[:length])

def aptamer(ligand, piece='whole'):
    """
    Construct aptamer sequences.

    Parameters
    ----------
    ligand: 'theo'
        Specify the aptamer to generate.  Right now only the theophylline 
        aptamer is known.

    piece: 'whole', '5', '3', or 'splitter'
        Specify which part of the aptamer to generate.  The whole aptamer 
        is returned by default, but each aptamer can be broken into a 
        5' half, a 3' half, and a splitter between those halves.  

    Returns
    -------
    aptamer: Construct
        The returned construct is given constraints, which can be used to force 
        RNAfold to approximate a ligand bound state.
    """

    # Get the right sequence for the requested aptamer.

    if ligand in ('th', 'theo', 'theophylline'):
        sequence_pieces   = 'AUACCAGCC', 'GAAA', 'GGCCCUUGGCAG'
        constraint_pieces = '.(.((((((', '....', ')))...))).).'

    elif ligand in ('3mx', '3-methylxanthine'):
        # Soukup, Emilsson, Breaker. Altering molecular recognition of RNA 
        # aptamers by allosteric selection. J. Mol. Biol. (2000) 298, 623-632.
        sequence_pieces   = 'AUACCAGCC', 'GAAA', 'GGCCAUUGGCAG'
        constraint_pieces = '.(.((((((', '....', ')))...))).).'

    elif ligand in ('tc', 'tet', 'tetracycline'):
        # Weigand, Suess. Tetracycline aptamer-controlled regulation of pre- 
        # mRNA splicing in yeast. Nucl. Acids Res. (2007) 35 (12): 4179-4185.
        #sequence_pieces   = 'GGCCUAAAACAUACCAGAU', 'GAAA', 'GUCUGGAGAGGUGAAGAAUACGACCACCUAGGCC'
        #constraint_pieces = '(((((........((((((', '....', '))))))..(((((...........))))))))))'

        # Win, Smolke. A modular and extensible RNA-based gene-regulatory 
        # platform for engineering cellular function. PNAS (2007) 104 (36): 
        # 14283-14288.
        #
        # Win & Smolke use a truncated tet aptamer to actually affect gene 
        # expression in vivo.  The Weigand & Suess aptamer has a stem on the 
        # end, which makes me skeptical that it would work for the purposes of 
        # this project.  
        sequence_pieces   = 'AAAACAUACCAGAU', 'UUCG', 'AUCUGGAGAAGGUGAAGAAUUCGACCACCU'
        constraint_pieces = '........((((((', '....', '))))))...(((((...........)))))'

    else:
        raise ValueError("no aptamer for '{}'".format(ligand))

    # Define the domains that make up the aptamer.

    aptamer_5 = Domain("aptamer/5'", sequence_pieces[0])
    aptamer_S = Domain("splitter", sequence_pieces[1])
    aptamer_3 = Domain("aptamer/3'", sequence_pieces[2])

    aptamer_5.constraints = constraint_pieces[0]
    aptamer_S.constraints = constraint_pieces[1]
    aptamer_3.constraints = constraint_pieces[2]

    aptamer_5.style = 'yellow', 'bold'
    aptamer_S.style = 'yellow', 'bold'
    aptamer_3.style = 'yellow', 'bold'

    aptamer_S.mutable = True

    # Assemble the aptamer domains into a single construct and return it.

    construct = Construct('aptamer')

    if piece == 'whole':
        construct += aptamer_5
        construct += aptamer_S
        construct += aptamer_3
    elif str(piece) == '5':
        construct += aptamer_5
    elif piece == 'splitter':
        construct += aptamer_S
    elif str(piece) == '3':
        construct += aptamer_3
    else:
        raise ValueError("must request 'whole', '5', '3', or 'splitter' piece of aptamer, not {}.".format(piece))

    return construct

def aptamer_insert(ligand, linker_len=0, splitter_len=0, repeat_factory=repeat,
        num_aptamers=1):

    insert = aptamer(ligand)

    # If multiple aptamers were requested, build them around the central one.

    for i in range(1, num_aptamers):
        insert.replace('splitter', aptamer(ligand))

    # If a splitter was requested, insert it into the middle of the aptamer.

    if splitter_len != 0:
        insert.replace('splitter', repeat_factory('splitter', splitter_len))

    # Add a linker between the aptamer and the sgRNA.

    try: linker_len_5, linker_len_3 = linker_len
    except TypeError: linker_len_5 = linker_len_3 = linker_len

    insert.prepend(repeat_factory("linker/5'", linker_len_5))
    insert.append(repeat_factory("linker/3'", linker_len_3))

    return insert

def hammerhead_l2(stem_len=5):
    if not 0 <= stem_len <= 5:
        raise ValueError("Stem III of the hammerhead ribozyme must be between 0 and 5 bp long.")
    offset = 5 - stem_len
    sequence_5 = (
            'GCUGU'
            'C'
            'ACCGGA'
            'UGUGCUU'
            'UCCGGU'
            'CUGAUGA'
            'GUCC'
            'GU'
    )
    sequence_3 = (
            'GA'
            'GGAC'
            'GAA'
            'ACAGC'
    )
    domains = (
            Domain("hammerhead/5'", sequence_5[offset:]),
            Domain("hammerhead/3'", sequence_3[:len(sequence_3)-offset]),
    )
    for domain in domains:
        domain.style = 'yellow', 'bold'
    return domains

def complementary_switch(target_seq):
    switch_domain = Domain('switch', reverse_complement(target_seq))
    on_domain = Domain('on', target_seq)
    off_domain = Domain('off', target_seq)
    return switch_domain, on_domain, off_domain

def wobble_switch(target_seq, favor_cutting, num_mutations=1):
    # Find all the positions where a wobble base pair could be made, i.e. all 
    # the positions in the "off" sequence that are either G or U.

    if favor_cutting:
        switch_domain = Domain('switch', reverse_complement(target_seq))
        for i, I in find_middlemost(target_seq, '([GU])', num_mutations):
            mutation = {'G':'U','U':'G'}[target_seq[i]] 
            switch_domain.mutate(I, mutation)
        on_domain = Domain('on', reverse_complement(switch_domain.seq))

    else:
        on_domain = Domain('on', target_seq)
        for i, I in find_middlemost(target_seq, '([AC])', num_mutations):
            mutation = {'C':'U','A':'G'}[target_seq[i]] 
            on_domain.mutate(i, mutation)
        switch_domain = Domain('switch', reverse_complement(target_seq))

    return switch_domain, on_domain, Domain('off', target_seq)

def mismatch_switch(target_seq, favor_cutting):
    middlemost = find_middlemost(target_seq, '[AU](.)[GC]|[GC](.)[AU]')
    mutations = {'A':'C','C':'C','G':'A','U':'C'}

    if favor_cutting:
        switch_domain = Domain('switch', reverse_complement(target_seq))
        for i, I in middlemost:
            switch_domain.mutate(I, mutations[target_seq[i]])
        on_domain = Domain('on', reverse_complement(switch_domain.seq))

    else:
        on_domain = Domain('on', target_seq)
        for i, I in middlemost:
            on_domain.mutate(i, mutations[complement(target_seq[i])])
        switch_domain = Domain('switch', reverse_complement(target_seq))

    return switch_domain, on_domain, Domain('off', target_seq)

def bulge_switch(target_seq, favor_cutting, bulge_seq='A'):
    i = len(target_seq) // 2
    
    if favor_cutting:
        switch_domain = Domain('switch', reverse_complement(target_seq))
        switch_domain.insert(i, bulge_seq)
        on_domain = Domain('on', reverse_complement(switch_domain.seq))

    else:
        on_domain = Domain('on', target_seq)
        on_domain.insert(i, bulge_seq)
        switch_domain = Domain('switch', reverse_complement(target_seq))

    return switch_domain, on_domain, Domain('off', target_seq)

def tunable_switch(target_seq, tuning_strategy=''):
    """
    Return three domains that comprise a switch.  The first domain ("switch") 
    is a sequence that can base pair with either of the two following domains, 
    the second domain ("on") is what the first should bind in the "on" state, 
    and the third domain ("off") is what the first should bind in the "off" 
    state.  
    
    By default, "switch" is perfectly complementary with both "on" and "off", 
    so it doesn't have a preference for one over the other.  You can tune the 
    switch by weakening the interactions it makes with one of its partners so 
    that it will prefer the other.  The tuning_strategy parameter specifies how 
    this should be done.  Each strategy is a 2-3 letter string.  The first 
    letter specifies what kind of mutation to make:

        w: Insert a wobble (GU) base pair.
        m: Insert a one nucleotide mismatch (1x1).
        b: Insert a one nucleotide bulge (1x0).

    Wobble base pairs are weaker perturbations and are only expected to shift 
    the equilibrium by a factor of 10.  Mismatches and bulges are stronger and 
    are both expected to shift the equilibrium by a factor of 100.

    The second letter specifies which state to weaken:
    
        x: More cutting, weaken the off state.
        o: Less cutting, weaken the on state.
    
    The meaning of the third letter depends on the chosen strategy (i.e. the 
    first letter):

        w: [0-9]+: Make the specified number of wobble mutations.
        b: g: Make the bulge a G instead on an A.  This should lead to a 
           slightly stronger activating effect.
    """

    if not tuning_strategy:
        return complementary_switch(target_seq)

    if tuning_strategy[0] not in 'wmb':
        raise ValueError("Tuning strategy must be one of 'wmb', not '{}'.".format(tuning_strategy[0]))
    if tuning_strategy[1] not in 'xo':
        raise ValueError("Desired tuning effect must be one of 'xo', not '{}'".format(tuning_strategy[1]))

    favor_cutting = True if tuning_strategy[1] == 'x' else False

    if tuning_strategy[0] == 'w':
        num_mutations = int(tuning_strategy[2:] or 1)
        return wobble_switch(target_seq, favor_cutting, num_mutations)
    if tuning_strategy[0] == 'm':
        return mismatch_switch(target_seq, favor_cutting)
    if tuning_strategy[0] == 'b':
        bulge_seq = 'G' if tuning_strategy == 'bxg' else 'A'
        return bulge_switch(target_seq, favor_cutting, bulge_seq)

def serpentine_insert(ligand, target_seq, target_end, tuning_strategy='',
        turn_seq='GAAA', num_aptamers=1):

    if not target_seq:
        raise ValueError('target_seq cannot be empty')

    switch_domain, on_domain, off_domain = tunable_switch(
            target_seq, tuning_strategy)

    domains = [
            Domain('turn', turn_seq),
            switch_domain,
            aptamer_insert(ligand, num_aptamers=num_aptamers),
            on_domain,
    ]

    if target_end == '3':
        domains.reverse()
        i, j = 0, 2
    else:
        i, j = 1, 3

    domains[i].expected_fold = '(' * len(domains[i])
    domains[j].expected_fold = ')' * len(domains[j])

    return Construct('serpentine', domains)

def circle_insert(ligand, target_seq, target_end, tuning_strategy='',
        num_aptamers=1):

    if not target_seq:
        raise ValueError('target_seq cannot be empty')

    switch_domain, on_domain, off_domain = tunable_switch(
            target_seq, tuning_strategy)

    domains = [
            on_domain,
            aptamer_insert(ligand, num_aptamers=num_aptamers),
            switch_domain,
    ]

    if target_end == '3':
        domains.reverse()

    domains[0].expected_fold = '(' * len(domains[0])
    domains[2].expected_fold = ')' * len(domains[2])
    
    return Construct('circle', domains)

def hammerhead_insert(ligand, mode, stem_len=5, num_aptamers=1):
    hammerhead_5, hammerhead_3 = hammerhead_l2(stem_len)
    domains = [hammerhead_5]

    if mode == 'on':
        domains += [
                Domain('switch', 'GUCC'),
                aptamer_insert(ligand, num_aptamers=num_aptamers),
                Domain('on', 'GGACG'),
                Domain('off', 'GGAC'),
        ]
    elif mode == 'off':
        domains += [
                Domain('switch', 'GUUGCUG'),
                aptamer_insert(ligand, num_aptamers=num_aptamers),
                Domain('off', 'CAGUGGAC'),
        ]

    domains += [hammerhead_3]
    return Construct('hammerhead', domains)


