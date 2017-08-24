#!/usr/bin/env python

from pprint import pprint
from .sequence import *
from .helpers import *

def t7_promoter(source='briner', extra_gua=0):
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

    sequence += extra_gua * 'G'

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

def spacer(name='none'):
    """
    Return the specified spacer sequence.

    Parameters
    ----------
    target: 'rfp', 'aavs', 'vegfa'
        The sequence to target.
    """
    aliases = {
            'rfp1': 'rfp',
            'gfp1': 'gfp',
            'k1': 'klein1',
            'k2': 'klein2',
    }
    spacers = {
            'none':   '',
            'n20':    'NNNNNNNNNNNNNNNNNNNN',
            'rfp':    'AACTTTCAGTTTAGCGGTCT',
            'rfp2':   'UGGAACCGUACUGGAACUGC',
            'gfp':    'CATCTAATTCAACAAGAATT',
            'gfp2':   'AGUAGUGCAAAUAAAUUUAA',
            'aavs':   'GGGGCCACTAGGGACAGGAT',
            'vegfa':  'GGGTGGGGGGAGTTTGCTCC',
            'klein1': 'GGGCACGGGCAGCTTGCCCG',
            'klein2': 'GTCGCCCTCGAACTTCACCT',
            'cf1':    'CCGGCAAGCTGCCCGTGCCC', # sgGFP9 (Christoff Fellman)
            'cf2':    'CAGGGTCAGCTTGCCGTAGG', # sgGFP8
            'cf3':    'CCTCGAACTTCACCTCGGCG', # sgGFP1
            'tdh1':   'AATAAGTATATAAAGACGGT',
            'tdh2':   'GACTAATAAGTATATAAAGA',
            'tdh3':   'ATATACTTATTAGTCAAGTA',
    }

    # Include the Doench16 spacers
    from os.path import join, dirname
    doench_tsv = join(dirname(__file__), 'doench_spacers.tsv')
    with open(doench_tsv) as file:
        for line in file:
            doench_name, spacer, score = line.split()
            spacers[doench_name] = spacer[4:24]

    try:
        sequence = spacers[aliases.get(name, name)]
    except KeyError:
        raise ValueError("Unknown spacer: '{}'".format(name))

    spacer = Domain('spacer', sequence)
    spacer.style = 'white', 'bold'

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

def aptamer(ligand, piece='whole', liu=False):
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

    affinity_uM = float('inf')

    # Get the right sequence for the requested aptamer.

    if ligand in ('th', 'theo', 'theophylline'):
        sequence_pieces         = 'AUACCAGCC', 'GAAA', 'GGCCCUUGGCAG'
        if liu: sequence_pieces = 'AUACCACGC', 'GAAA', 'GCGCCUUGGCAG'
        constraint_pieces       = '.((((.(((', '....', ')))....)))).'
        affinity_uM = 0.32

    elif ligand in ('gtheoc'):
        # The theophylline aptamer, bracketed by a GC base pair.  This 
        # construct is more convenient to use with ViennaRNA, because a 
        # bracketing base pair is required to make a constraint.
        sequence_pieces   = 'GAUACCAGCC', 'GAAA', 'GGCCCUUGGCAGC'
        constraint_pieces = '(.((((.(((', '....', ')))....)))).)'
        affinity_uM = 0.32

    elif ligand in ('3', '3mx', '3-methylxanthine'):
        # Soukup, Emilsson, Breaker. Altering molecular recognition of RNA 
        # aptamers by allosteric selection. J. Mol. Biol. (2000) 298, 623-632.
        sequence_pieces   = 'AUACCAGCC', 'GAAA', 'GGCCAUUGGCAG'
        constraint_pieces = '.(.((((((', '....', ')))...))).).'

    elif ligand in ('r', 'tmr', 'tetramethylrosamine', 'mg', 'malachite green'):
        # Baugh, Grate, Wilson. 2.8Å structure of the malachite green aptamer.  
        # JMB (2000) 301:1:117-128.

        # This aptamer was used to make riboswitches, but with luciferase and 
        # not RFP, possibly because TMR is a fluorescent dye: Borujeni et al.  
        # Automated physics-based design of synthetic riboswitches from diverse 
        # RNA aptamers. Nucl.  Acids Res.  (2016) 44:1:1-13.

        # I can't find any commercial TMR.  Sigma used to sell it as product 
        # number T1823, but has since discontinued it.
        sequence_pieces   = 'CCGACUGGCGAGAGCCAGGUAACGAAUG',
        constraint_pieces = '(...(((((....))))).........)',

    elif ligand in ('tpp', 'thiamine', 'thiamine pyrophosphate'):
        # Winkler, Hahvi, Breaker. Thiamine derivatives bind messenger RNAs 
        # directly to regulate bacterial gene expression. Nature (2002) 
        # 419:952-956.

        # The sequence I've copied here is the ThiM 91 fragment from Winkler et 
        # al.  Weiland et al. used almost the same sequence, but they mutated 
        # the last nucleotide from A to U to break a base pair.

        # Winker et al used "M9 glucose minimal media (plus 50 μg/mL vitamin 
        # assay Casamino acids; Difco)" with or without 100 μM thiamine for 
        # their in vivo assays (figure 4b, bottom).  The "vitamin assay" means 
        # the casein digest was treated to remove certain vitamins; presumably 
        # this is an important detail.

        # Weiland et al. used M63 media with or without 1 mM thiamine for their 
        # in vivo assays.  This is a little confusing to me because the M63 
        # recipe I found contains thiamine.  Also, the titrations in figure 3B 
        # and 3C only go to 50 μM (and saturate around 1 μM).

        # My plan is to use M9 media with glucose and "vitamin assay" Casamino 
        # acids, with and without 100 μM thiamine.
        sequence_pieces   = 'UCGGGGUGCCCUUCUGCGUGAAGGCUGAGAAAUACCCGUAUCACCUGAUCUGGAUAAUGCCAGCGUAGGGAA',
        constraint_pieces = '(..(((((.(((((.....)))))........)))))......((((..((((......))))..))))..)',
        affinity_uM = 0.0324 # (interpolated from figure 2b in Winkler et al.)

    elif ligand in ('a', 'add', 'adenine'):
        # Serganov et al. Structural Basis for discriminative regulation of 
        # gene expression by adenine- and guanine-sensing mRNAs. Chemistry & 
        # Biology (2004) 11:1729-1741.

        # I truncated 7 base pairs that weren't interacting with the ligand 
        # from the end of the construct.  I haven't been able to find an 
        # example of the adenine aptamer being used in a riboswitch to see if 
        # this is what other people have done, but Nomura et al. made 
        # essentially the same truncation to the highly homologous guanine 
        # aptamer when using it to make an allosteric ribozyme, so I'm pretty 
        # confident that this could work.

        # Dixon et al. used M9 + 0.4% glucose + 2 mg/mL cas-amino acids + 0.1 
        # mg/mL thiamine.  This is a higher concentration of cas-amino acids 
        # than Winkler et al. use for the TPP aptamer, but this is much more in 
        # line with the standard protocols.
        # 
        # The ligand was also in some amount of DMSO, but I'm not sure how 
        # much.  The solubility of adenine in water is 7.6 mM, so maybe the 
        # DMSO was only necessary for some of their other ligands.
        sequence_pieces   = 'UAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUA',
        constraint_pieces = '((...(((((((.......)))))))........((((((.......))))))..))',

    elif ligand in ('b', 'amm', 'ammeline'):
        # Dixon et al. Reengineering orthogonally selective riboswitches. PNAS 
        # (2010) 107:7:2830-2835.

        # This is the M6 construct, which is just the adenine aptamer from 
        # above with U47C and U51C.  The affinity measurement is actually for 
        # M6'', because it was not measured for M6.
        sequence_pieces   = 'UAUAAUCCUAAUGAUAUGGUUUGGGAGCUUCCACCAAGAGCCUUAAACUCUUGAUUA',
        constraint_pieces = '((...(((((((.......)))))))........((((((.......))))))..))',
        affinity_uM = 1.19

    elif ligand in ('g', 'gua', 'guanine'):
        # Nomura, Zhou, Miu, Yokobayashi. Controlling mammalian gene expression 
        # by allosteric Hepatitis Delta Virus ribozymes. ACS Synth. Biol.  
        # (2013) 2:684-689.

        # Nomura et al. used guanine at 500 μM, but I still see toxicity at 
        # this concentration.  I think I'm going to use 250 μM instead.
        sequence_pieces   = 'UAUAAUCGCGUGGAUAUGGCACGCAAGUUUCUACCGGGCACCGUAAAUGUCCGACUA',
        constraint_pieces = '((...(.(((((.......))))).)........((((((.......))))))..))',
        affinity_uM = 0.005

    elif ligand in ('fmn', 'flavin', 'flavin mononucleotide'):
        # Soukup, Breaker. Engineering precision RNA molecular switches. PNAS 
        # (1999) 96:3584-3589.  

        # I can't find any examples of anyone using this aptamer in vivo.
        sequence_pieces   = 'GAGGAUAUGCUUCGGCAGAAGGC',
        constraint_pieces = '(......(((....))).....)',

    elif ligand in ('m', 'ms2', 'ms2 coat protein'):
        # Qi, Lucks, Liu, Mutalik, Arkin. Engineering naturally occurring 
        # trans-acting non-coding RNAs to sense molecular signals. Nucl. Acids 
        # Res. (2012) 40:12:5775-5786. Sequence in supplement.

        # I can't really figure out which MS2 aptamer people use for synthetic 
        # biology.  All the papers I've read agree that the aptamer has one 
        # stem and three unpaired adenosines.  The sequences from Romaniuk, 
        # Convery, and Qi actually have the same stem, they just differ in the 
        # loop.  The sequences from Batey and Culler are exactly the same, but 
        # different from those in the other papers.

        # The loop from Romaniuk and Convery is AUUA (the wildtype sequence) 
        # while the loop from Qi is ACCA.  I'm inclined to use ACCA because Qi 
        # was doing synthetic biology and because Convery mentions that the 
        # natural consensus sequence for the loop is ANYA, a standard tetraloop 
        # which doesn't preclude ACCA.

        # I should consider making the N55K mutation to the coat protein 
        # itself.  One of the plasmids on AddGene mentioned that this mutation 
        # increases affinity for the aptamer.  That plasmid was for mammalian 
        # expression, and so far I haven't seen this assertion corroborated for 
        # bacterial systems.
        sequence_pieces   = 'AACAUGAGGACCACCCAUGUU',
        constraint_pieces = '((((((.((....))))))))',

    elif ligand in ('bca', 'beta-catenin'):
        # Culler, Hoff, Smolke. Reprogramming cellular behavior with rna 
        # controllers responsive to endogenous proteins. Science (2010) 
        # 330:6008:1251-1255.
        sequence_pieces = 'AGGCCGATCTATGGACGCTATAGGCACACCGGATACTTTAACGATTGGCT',
        raise NotImplementedError

    elif ligand in ('tc', 'tet', 'tetracycline'):
        # Wittmann and Suess.  Selection of tetracycline inducible 
        # self-cleaving ribozymes as synthetic devices for gene regulation in 
        # yeast.  Mol BioSyst (2011) 7:2419-2427.

        # The authors used 100 μM tetracycline in yeast.  I've seen other 
        # papers that used as much as 250 μM.
        sequence_pieces   = 'AAAACAUACCAGAUUUCGAUCUGGAGAGGUGAAGAAUACGACCACCU',
        constraint_pieces = '(.......((((((....))))))...((((...........)))))',

        # Müller, Weigand, Weichenrieder, Suess. Thermodynamic characterization 
        # of an engineered tetracycline-binding riboswitch. Nucleic Acids 
        # Research (2006) 34:9:2607-2617.
        affinity_uM = 0.00077 # 770 pM

    elif ligand in ('neo', 'neomycin'):
        # Weigand, Sanchez, Gunnesch, Zeiher, Schroeder, Suess. Screening for 
        # engineered neomycin riboswitches that control translation initiation.  
        # RNA (2008) 14:89-97.

        # The authors show that the aptamer consists of two domains: one that 
        # binds neomycin and one which is just a stem.  Both are important for 
        # regulating gene expression in their system, which is the 5'-UTR of an 
        # mRNA.  However, here I only include the ligand-binding domain.  The 
        # length and composition of the stem domain is probably application 
        # dependent, and that's what I need to pull out of directed evolution.
        #
        # The authors used 100 μM neomycin.  Yeast were grown at 28°C for 48h 
        # in 5 mL minimal media.
        sequence_pieces   = 'GCUUGUCCUUUAAUGGUCC',
        constraint_pieces = '(.....((......))..)',

    elif ligand in ('asp', 'aspartame'):
        # Ferguson et al. A novel strategy for selection of allosteric 
        # ribozymes yields RiboReporter™ sensors for caffeine and aspartame.  
        # Nucl. Acids Res. (2004) 32:5
        sequence_pieces   = 'CGGTGCTAGTTAGTTGCAGTTTCGGTTGTTACG',
        constraint_pieces = '((.............................))',

    elif ligand in ('caf', 'caffeine'):
        # Ferguson et al. A novel strategy for selection of allosteric 
        # ribozymes yields RiboReporter™ sensors for caffeine and aspartame.  
        # Nucl. Acids Res. (2004) 32:5
        sequence_pieces   = 'GATCATCGGACTTTGTCCTGTGGAGTAAGATCG',
        constraint_pieces = '.................................',

    else:
        raise ValueError("no aptamer for '{}'".format(ligand))

    # Check for obvious entry errors in the aptamer sequences.

    if len(sequence_pieces) not in (1, 3):
        raise AssertionError("{} has {} sequence pieces, not 1 or 3.".format(ligand, len(sequence_pieces)))
    if len(sequence_pieces) != len(constraint_pieces):
        raise AssertionError("{} has {} sequence pieces and {} constraint pieces.".format(ligand, len(sequence_pieces), len(constraint_pieces)))
    if len(''.join(sequence_pieces)) != len(''.join(constraint_pieces)):
        raise AssertionError("the {} sequence has a different length than its constraints.".format(ligand))

    # Define the domains that make up the aptamer.

    if len(sequence_pieces) == 1:
        aptamer = Domain("aptamer", sequence_pieces[0])
        aptamer.constraints = constraint_pieces[0]
        aptamer.style = 'yellow', 'bold'
        aptamer.kd = affinity_uM

    if len(sequence_pieces) == 3:
        aptamer_5 = Domain("aptamer/5'", sequence_pieces[0])
        aptamer_S = Domain("aptamer/splitter", sequence_pieces[1])
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

    if len(sequence_pieces) == 1:
        construct += aptamer

    if len(sequence_pieces) == 3:
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
        insert.replace('aptamer/splitter', aptamer(ligand))

    # If a splitter was requested, insert it into the middle of the aptamer.

    if splitter_len != 0:
        insert.replace('aptamer/splitter', repeat_factory('aptamer/splitter', splitter_len))

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

def random_insert(ligand, linker_len_5, linker_len_3, num_aptamers=1):
    return aptamer_insert(
            ligand,
            linker_len=(linker_len_5, linker_len_3),
            repeat_factory=lambda name, len: Domain(name, 'N' * len),
            num_aptamers=num_aptamers,
    )


