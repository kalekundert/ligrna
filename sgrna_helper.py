#!/usr/bin/env python3

import nonstdlib

class Construct:

    def __init__(self, sequence='', tag=None, name='', constraints=''):
        self.name = name
        self._sequence = sequence

        self._tags = {i: tag for i in range(len(self))}

        if constraints:
            self._constraints = constraints
        else:
            self._constraints = '.' * len(sequence)

        if len(self.constraints) != len(self.seq):
            raise ValueError("constraints don't match sequence")

    def __repr__(self):
        return 'Construct({})'.format(self._sequence)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return repr(self)

    def __len__(self):
        return len(self._sequence)

    def __eq__(self, sequence):
        return self._sequence == sequence

    def __add__(self, construct):
        result = Construct()
        result.append(self)
        result.append(construct)
        result.name = '{}+{}'.format(self.name, construct.name)
        return result

    def __iadd__(self, construct):
        self.append(construct)
        return self

    @property
    def function_name(self):
        factory, arguments = parse_name(self.name)
        return '{}({})'.format(factory, ','.join(str(x) for x in arguments))

    @property
    def underscore_name(self):
        import re
        return re.sub('[^a-zA-Z0-9]+', '_', self.name).strip('_')

    @property
    def seq(self):
        return self._sequence

    @property
    def dna(self):
        return self._sequence.replace('U', 'T')

    @property
    def rna(self):
        return self._sequence.replace('T', 'U')

    @property
    def indices(self):
        return range(len(self._sequence))

    @property
    def constraints(self):
        return self._constraints

    def mass(self, polymer='rna'):
        sequence = self.seq.upper()

        a = sequence.count('A')
        c = sequence.count('C')
        g = sequence.count('G')
        t = u = sequence.count('T') + sequence.count('U')

        if polymer == 'rna':
            return (a * 329.2) + (u * 306.2) + (c * 305.2) + (g * 345.2) + 159
        elif polymer == 'dna':
            return ((a + t) * 617.4) + ((g + c) * 618.4) + 158
        elif polymer == 'ssdna':
            return (a * 313.2) + (t * 304.2) + (c * 289.2) + (g * 329.2) + 79
        else:
            raise ValueError("unknown polymer type: '{}'".format(polymer))

    def show(self, style=None, start=None, end=None, pad=True, labels=True, dna=False, rna=False, rev_com=False, color='auto'):

        # Choose default colors if none are explicitly given.

        if style is None:
            style = {
                    'rfp': 'yellow',
                    'aavs': 'yellow',
                    'vegfa': 'yellow',
                    'lower_stem': 'green',
                    'upper_stem': 'blue',
                    'nexus': 'red',
                    'hairpins': 'magenta',
                    'aptamer': ('white', 'bold'),
            }

        # Figure out which part of the construct to display.

        if dna: sequence = self.dna
        elif rna: sequence = self.rna
        else: sequence = self._sequence
            
        if start is None: start = 0
        if end is None: end = len(self)

        sequence = sequence[start:end]

        if rev_com: sequence = complement(sequence)

        # Print out ever base in the appropriate color.

        if pad: nonstdlib.write(' ' * start)
        if labels: nonstdlib.write("5'-" if not rev_com else "3'-")
        
        for i, base in enumerate(sequence, start):
            tag = self._tags[i]
            color_weight = style.get(tag, 'normal')
            if isinstance(color_weight, str):
                color_weight = color_weight, 'normal'
            nonstdlib.write_color(base, *color_weight, when=color)

        if labels: nonstdlib.write("-3'" if not rev_com else "-5'")
        nonstdlib.write('\n')

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def prepend(self, construct):
        self.insert(construct, 0)
        return self

    def append(self, construct):
        self.insert(construct, len(self))
        return self

    def append_with_linker(self, construct):
        self.insert_with_linker(construct, len(self))
        return self

    def insert(self, construct, index):
        head = 0
        new_sequence = ''
        new_tags = {}
        new_constraints = ''

        for i in range(index):
            new_sequence += self._sequence[i]
            new_tags[head] = self._tags[i]
            new_constraints += self._constraints[i]
            head += 1

        for i in range(len(construct)):
            new_sequence += construct._sequence[i]
            new_tags[head] = construct._tags[i]
            new_constraints += construct._constraints[i]
            head += 1

        for i in range(index, len(self._sequence)):
            new_sequence += self._sequence[i]
            new_tags[head] = self._tags[i]
            new_constraints += self._constraints[i]
            head += 1

        self._sequence = new_sequence
        self._tags = new_tags
        self._constraints = new_constraints

        return self

    def delete(self, start=..., end=...):
        head = 0
        new_sequence = ''
        new_tags = {}
        new_constraints = ''

        if start is ...: start = 0
        if start < 0: start = len(self) - abs(start)
        if end is ...: end = len(self)
        if end < 0: start = len(self) - abs(end)

        for i in range(start):
            new_sequence += self._sequence[i]
            new_tags[head] = self._tags[i]
            new_constraints += self._constraints[i]
            head += 1

        for i in range(end, len(self._sequence)):
            new_sequence += self._sequence[i]
            new_tags[head] = self._tags[i]
            new_constraints += self._constraints[i]
            head += 1

        self._sequence = new_sequence
        self._tags = new_tags
        self._constraints = new_constraints

        return self

    def replace(self, start, end, construct):
        self.delete(start, end)
        self.insert(construct, start)
        return self

    def mutate(self, index, base):
        self._sequence = (
                self._sequence[:index] +
                base +
                self._sequence[index+1:]
        )

    def pad(self, length, repeat_factory):
        self.insert(repeat_factory(length), 0)
        self.insert(repeat_factory(length), len(self))
        return self



def from_name(name):
    construct = Construct()
    names = []

    for factory, arguments in parse_name(name):
        if factory not in globals():
            raise ValueError("No designs named '{}'.".format(factory))

        fragment = globals()[factory](*arguments)
        names.append(fragment.name)
        construct += fragment

    construct.name = '+'.join(x for x in names if x)
    return construct

def parse_name(name):
    import re

    def cast_if_necessary(x):
        try: return int(x)
        except: return x


    name = name.strip()
    sub_names = []

    if not name:
        raise ValueError("Can't parse empty name.")

    for sub_name in name.split('+'):
        tokens = re.findall('[a-zA-Z0-9]+', sub_name)
        factory = tokens[0]
        arguments = [cast_if_necessary(x) for x in tokens[1:]]
        sub_names.append((factory, arguments))

    return sub_names

def wt_sgrna(target='aavs'):
    sgrna = Construct(name='wt sgrna')

    if target == 'rfp':
        sgrna += Construct('AACUUUCAGUUUAGCGGUCU', target)
    elif target == 'aavs':
        sgrna += Construct('GGGGCCACTAGGGACAGGAT', target)
    elif target == 'vegfa':
        sgrna += Construct('GGGTGGGGGGAGTTTGCTCC', target)
    else:
        raise ValueError("Unknown target: '{}'".format(target))

    sgrna += Construct('GUUUUA', 'lower_stem')
    sgrna += Construct('GA', 'bulge')
    sgrna += Construct('GCUA', 'upper_stem')
    sgrna += Construct('GAAA')
    sgrna += Construct('UAGC', 'upper_stem')
    sgrna += Construct('AAGU', 'bulge')
    sgrna += Construct('UAAAAU', 'lower_stem')
    sgrna += Construct('AAGGCUAGUCCGU', 'nexus')
    sgrna += Construct('UAUCA')
    sgrna += Construct('ACUUGAAAAAGU', 'hairpins')
    sgrna += Construct('G')
    sgrna += Construct('GCACCGAGUCGGUGC', 'hairpins')
    sgrna += Construct('UUUUUU')
    return sgrna

def dead_sgrna(target='aavs'):
    sgrna = wt_sgrna(target)
    sgrna.name = 'dead sgrna'
    sgrna.mutate(52, 'C')
    sgrna.mutate(53, 'C')
    return sgrna

def aptamer(ligand, piece='whole'):
    """
    Construct aptamer sequences.

    Parameters
    ----------
    ligand: 'theo'
        Specify the aptamer to generate.  Right now only the theophylline 
        aptamer is known.

    piece: 'whole', '5', '3', or 'linker'
        Specify which part of the aptamer to generate.  The whole aptamer 
        is returned by default, but each aptamer can be broken into a 
        5' half, a 3' half, and a linker between those halves.  

    Returns
    -------
    aptamer: Construct
        The returned construct is given constraints, which can be used to force 
        RNAfold to approximate a ligand bound state.
    """

    # Get the right sequence for the requested aptamer.

    if ligand in ('th', 'theo', 'theophylline'):
        ligand = 'theophylline'
        sequence_pieces   = 'AUACCAGCC', 'GAAA', 'GGCCCUUGGCAG'
        constraint_pieces = '(((((.(((', '....', ')))....)))))'
    else:
        raise ValueError("no aptamer for '{}'".format(ligand))

    # Construct and return the requested piece of the requested aptamer.

    if piece == 'whole':
        sequence = ''.join(sequence_pieces)
        constraints = ''.join(constraint_pieces)
    elif str(piece) == '5':
        sequence = sequence_pieces[0]
        constraints = constraint_pieces[0]
    elif piece == 'linker':
        sequence = sequence_pieces[1]
        constraints = constraint_pieces[1]
    elif str(piece) == '3':
        sequence = sequence_pieces[2]
        constraints = constraint_pieces[2]
    else:
        raise ValueError("must request 'whole', '5', '3', or 'linker' piece of aptamer, not {}.".format(piece))

    aptamer = Construct(sequence, 'aptamer', constraints=constraints)
    aptamer.name = ligand
    return aptamer

def theophylline_aptamer(piece='whole'):
    return aptamer('theo', piece)

def t7_promoter(source='briner'):
    if source == 'igem':
        # The "T7 consensus -10 and rest" sequence from IGEM:
        # http://parts.igem.org/Promoters/Catalog/T7
        promoter = Construct('TAATACGACTCACTATA', 't7')

    elif source == 'briner':
        # The T7 sequence used by Briner et al. (2014):
        promoter = Construct('TATAGTAATAATACGACTCACTATAG', 't7')

    else:
        raise ValueError("Unknown T7 sequence: '{}'".format(source))

    promoter.name = 't7'
    return promoter

def aavs_target():
    return Construct(
            'CCCCGTTCTCCTGTGGATTCGGGTCACCTCTCACTCCTTTCATTTGGGCA'
            'GCTCCCCTACCCCCCTTACCTCTCTAGTCTGTGCTAGCTCTTCCAGCCCC'
            'CTGTCATGGCATCTTCCAGGGGTCCGAGAGCTCAGCTAGTCTTCTTCCTC'
            'CAACCCGGGCCCCTATGTCCACTTCAGGACAGCATGTTTGCTGCCTCCAG'
            'GGATCCTGTGTCCCCGAGCTGGGACCACCTTATATTCCCAGGGCCGGTTA'
            'ATGTGGCTCTGGTTCTGGGTACTTTTATCTGTCCCCTCCACCCCACAGTG'
            'GGGCCACTAGGGACAGGATTGGTGACAGAAAAGCCCCATCCTTAGGCCTC'
            'CTCCTTCCTAGTCTCCTGATATTGGGTCTAACCCCCACCTCCTGTTAGGC'
            'AGATTCCTTATCTGGTGACACACCCCCATTTCCTGGAGCCATCTCTCTCC'
            'TTGCCAGAACCTCTAAGGTTTGCTTACGATGGAGCCAGAGAGGAT', name='aavs')

def repeat(length, pattern='UUUCCC'):
    sequence = pattern * (1 + length // len(pattern))
    return Construct(sequence[:length])

def smart_repeat(length, ligand=None):
    from itertools import product
    from more_itertools import pairwise
    from collections import Counter

    # Find the least common pair of RNA nucleotides in a collections.Counter 
    # object.

    def least_common(counter, first_nuc=None):
        least_common = None
        rna_nucs = 'UCAG'  # In the order that ties will be resolved.
        for pair in product(first_nuc or rna_nucs, rna_nucs):
            if not least_common or counter[pair] < counter[least_common]:
                least_common = pair
        return least_common if first_nuc is None else least_common[1]

    
    # Count how often each pair of nucleotides appears in the given reference 
    # sequences.

    constructs = [wt_sgrna()]
    if aptamer: constructs.append(aptamer(ligand))

    counter = Counter()
    for construct in constructs:
        for pair in pairwise(construct.rna):
            counter[pair] += 1

    # Compose a repeat that exclusively contains the least commonly seen pairs 
    # of nucleotides.

    repeat = ''.join(least_common(counter))
    while len(repeat) < length:
        repeat += least_common(counter, repeat[-1])
    return Construct(repeat[:length])

def upper_stem_insertion(N, linker_len=0, spacer_len=0):
    """
    Insert the aptamer into the upper stem region of the sgRNA.

    The upper stem region of the sgRNA is very tolerant to mutation.  In the 
    natural CRISPR/Cas system, this stem is actually where the two strands of  
    guide RNA (crRNA and tracrRNA) come together.

    Parameters
    ----------
    N: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.  The aptamer will be inserted 
        between the two ends of the stem.

    linker_len: int
        Indicate how many base pairs should separate the aptamer from the upper 
        stem.  The linker sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    if spacer_len != 0:
        args = N, linker_len, spacer_len
    else:
        args = N, linker_len

    return make_insertion(
            'us(' + ','.join(str(x) for x in args) + ')',
            28 + N,
            40 - N,
            linker_len=linker_len,
            spacer_len=spacer_len,
    )

def lower_stem_insertion(N, linker_len=0):
    """
    Insert the aptamer into the lower stem region of the sgRNA.

    Parameters
    ----------
    N: int
        Indicate how many of the 6 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 6, although in practice I only 
        expect to use values greater than 4 or 5.  Shorter than that and you'll 
        almost certainly interfere with normal Cas9 binding.

    linker_len: int
        Indicate how many base pairs should separate the aptamer from the upper 
        stem.  The linker sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    if not 0 <= N <= 6:
        raise ValueError("Location for lower stem insertion must be between 0 and 6, not {}.".format(N))

    return make_insertion(
            'ls({},{})'.format(N, linker_len),
            20 + N,
            50 - N,
            linker_len=linker_len,
    )

def nexus_insertion(linker_len=0):
    """
    Insert the aptamer into the nexus region of the sgRNA.

    The nexus is a short (2 bp) stem connected by 5 residues with irregular 
    secondary structure.  Briner et al. (2014) and Nishimasu et al. (2014) both 
    studied how mutations to this area can affect binding, but the results 
    aren't easy to rationalize.  Either one of the stem base pairs, but not 
    both, can be mutated to AU (both are naturally GC) without affecting 
    function.  Mutations were also made to 4 of the 5 positions with irregular 
    structure (sometimes in conjunction with mutations elsewhere that weren't 
    obviously compensatory) and all of those mutants were functional.
    
    My takeaway is that replacing the 5 irregular residues with the aptamer and 
    a variable length linker might be a good strategy.  For now, I'm going to 
    neglect the possibility of keeping any of the 5 irregular nexus residues.  
    There are of course many ways to do that, but no reason to think that one 
    would be more promising that any other.

    Parameters
    ----------
    linker_len: int
        Indicate how many base pairs should separate the aptamer from the nexus 
        region stem.  The linker sequence will have a UUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    return make_insertion(
            'nx({})'.format(linker_len),
            54,
            59,
            linker_len=linker_len,
            repeat_factory=lambda n: repeat(n, 'U'),
    )
    
def nexus_insertion_2(N, M, spacer_len=0, num_aptamers=1):
    """
    Insert the aptamer into the nexus region of the sgRNA.

    This design strategy expands upon the original nexus_insertion() function, 
    which produced promising initial hits.  This strategy allows more control 
    over where the aptamer is inserted, by having the user specify the number 
    of nucleotides to keep (N and M) on both sides of the nexus.  This strategy 
    also places the repeat sequence inside the aptamer rather than around it, 
    and allows for more than one aptamer to be chained together.

    Parameters
    ----------
    N: int
        The number of base pairs to keep on the 5' side of the nexus, starting 
        from the base of the hairpin at position 53.

    M: int
        The number of base pairs to keep on the 3' side of the nexus, starting 
        from the base of the hairpin at position 61.

    spacer_len: int
        The number of base pairs to insert into the middle of the aptamer.  The 
        linker will have the sequence 'UCGUCG...', which was chosen because it 
        has very low complementarity with the rest of the design.

    num_aptamers: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    Returns
    -------
    sgRNA: Construct
    """

    # Make sure the arguments have reasonable values.

    min_spacer_len = len(aptamer('theo', 'linker'))

    if not 0 <= N <= 4:
        raise ValueError("nxx: N must be between 0 and 4, not {}".format(N))
    if not 0 <= M <= 5:
        raise ValueError("nxx: M must be between 0 and 5, not {}".format(N))
    if 0 < spacer_len <= min_spacer_len:
        raise ValueError("nxx: spacer_len must be longer than {} (the natural linker length).".format(min_spacer_len))
    if num_aptamers < 1:
        raise ValueError("nxx: Must have at least 1 aptamer")

    # Figure out what to name the construct.  Make an effort to exclude 
    # arguments that the user didn't actually specify from the name.

    if num_aptamers != 1:
        args = N, M, spacer_len, num_aptamers
    elif spacer_len != 0:
        args = N, M, spacer_len
    else:
        args = N, M

    name = 'nxx({})'.format(','.join(str(x) for x in args))

    # Create and return the construct using a helper function.

    return make_insertion(
            name,
            52 + N,
            61 - M,
            spacer_len=spacer_len,
            num_aptamers=num_aptamers,
    )

def hairpin_replacement(N):
    """
    Remove a portion of the 3' terminal hairpins and replace it with the 
    aptamer.
    
    Parameters
    ----------
    N: int
        Indicate how much of the 3' terminal hairpins should be kept, with the 
        counting starting at position 63.  An N of 33 therefore specifies that 
        the whole sgRNA should be kept (excluding the poly-U tail) and that the 
        aptamer should simply be added onto the end.  Values larger than 33 
        specify that a linker should be inserted between the sgRNA and the 
        aptamer.  Values smaller than 33 specify that some residues should be 
        truncated from the 3' end of the sgRNA.  The expected range for this 
        parameter is roughly 17-33.

    Returns
    -------
    sgRNA: Construct
        The specified construct will be returned, with a hexa-uracil tail will 
        added to the end for the benefit of the T7 polymerase.
    """

    # Remove the UUUUUU tail from the wildtype sgRNA.  This tail will be added 
    # back, in a UUUCCC pattern to avoid too many consecutive uracils, if N is 
    # past the end of the sgRNA proper.

    design = Construct(name='hp({})'.format(N))
    design += wt_sgrna().delete(-6, ...)

    insertion_site = 63 + N

    if insertion_site < len(design):
        design.delete(insertion_site, ...)

    if insertion_site > len(design):
        design += repeat(insertion_site - len(design))

    design += theophylline_aptamer()
    design += Construct('UUUUUU')

    return design

def induced_dimerization(half, N):
    """
    Split the guide RNA into its two naturally occurring halves, and use the 
    aptamer to bring those halves together in the presence of the ligand.  The 
    aptamer replaces some or all of the upper stem.  We have already observed 
    that an sgRNA with the upper stem fully replaced by the theophylline 
    aptamer is fully functional, so the design should work if the ligand 
    successfully induces dimerization.

    Parameters
    ----------
    half: 5 or 3
        Indicate which half of the split construct to return.  '5' and '3' 
        refer to the 5' and 3' halves, respectively.

    N: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.

    Returns
    -------
    sgRNA: Construct
    """

    # Make sure the arguments make sense.

    half = str(half)
    N = int(N)

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    # Construct and return the requested sequence.

    design = Construct(name='id({},{})'.format(half, N))

    if half == '5':
        design += wt_sgrna().delete(start=28+N)
        design += theophylline_aptamer('5')

    elif half == '3':
        design += theophylline_aptamer('3')
        design += wt_sgrna().delete(end=40-N)

    else:
        raise ValueError("Half for induced dimerization must be either 5 (for the 5' half) or 3 (for the 3' half), not '{}'.".format(half))

    return design

def make_insertion(name, insert_begin, insert_end,
        linker_len=0,
        spacer_len=0,
        repeat_factory=repeat,
        num_aptamers=1,
        ligand='theo'):

    design = Construct(name=name)
    design += wt_sgrna()

    # If a spacer was requested, insert it into the middle of the aptamer.

    if spacer_len == 0:
        insert = aptamer(ligand)
    else:
        insert = aptamer(ligand, '5')
        insert += repeat_factory(spacer_len) 
        insert += aptamer(ligand, '3')

    # If multiple aptamers were requested, build them around the central one.

    for i in range(1, num_aptamers):
        insert.prepend(aptamer(ligand, '5'))
        insert.append(aptamer(ligand, '3'))

    # If a linker between the aptamer and the sgRNA was requested, add it.

    insert.pad(linker_len, repeat_factory)

    # Insert the aptamer into the sgRNA and return the resulting construct.

    design.replace(insert_begin, insert_end, insert)
    return design

def complement(sequence):
    complements = str.maketrans('ACTG', 'TGAC')
    return sequence.translate(complements)

def reverse_complement(sequence):
    return complement(sequence[::-1])


## Abbreviations
wt = wt_sgrna
dead = dead_sgrna
t7 = t7_promoter
th = theo = theophylline_aptamer
aavs = aavs_target
us = upper_stem_insertion
ls = lower_stem_insertion
nx = nexus_insertion
nxx = nexus_insertion_2
hp = hairpin_replacement
id = induced_dimerization


def test_construct_constraints():
    import pytest

    with pytest.raises(ValueError): Construct('AA', constraints='.')
    with pytest.raises(ValueError): Construct('AA', constraints='...')

    ins = Construct('AA', constraints='()')
    seq = 'AAAAAAAAAA'

    assert ins.constraints == '()'
    assert Construct(seq).constraints == '..........'
    assert Construct(seq).prepend(ins).constraints == '()..........'
    assert Construct(seq).append(ins).constraints == '..........()'
    assert Construct(seq).insert(ins, 5).constraints == '.....().....'
    assert Construct(seq).replace(3, 5, ins).constraints == '...().....'

def test_wt_sgrna():
    assert from_name('wt').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('wt_rfp').seq == 'AACUUUCAGUUUAGCGGUCUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('wt_vegfa').seq == 'GGGTGGGGGGAGTTTGCTCCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_dead_sgrna():
    assert from_name('dead').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAACCCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('dead_rfp').seq == 'AACUUUCAGUUUAGCGGUCUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAACCCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('dead_vegfa').seq == 'GGGTGGGGGGAGTTTGCTCCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAACCCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_theophylline_aptamer():
    assert theophylline_aptamer().seq == 'AUACCAGCCGAAAGGCCCUUGGCAG'

def test_repeat():
    assert repeat(1).seq == 'U'
    assert repeat(2).seq == 'UU'
    assert repeat(3).seq == 'UUU'
    assert repeat(4).seq == 'UUUC'
    assert repeat(5).seq == 'UUUCC'
    assert repeat(6).seq == 'UUUCCC'
    assert repeat(7).seq == 'UUUCCCU'

def test_smart_repeat():
    assert smart_repeat(10, 'theo') == 'UCGUCGUCGU'

def test_from_name():
    equivalent_constructs = [
            from_name('us(4)'),
            from_name('us(4,0)'),
            from_name('us(4, 0)'),
            from_name('us 4'),
            from_name('us 4 0'),
            from_name('us/4'),
            from_name('us/4/0'),
            from_name('us-4'),
            from_name('us-4-0'),
            from_name('us_4'),
            from_name('us_4_0'),
    ]

    for construct in equivalent_constructs:
        assert construct.seq == equivalent_constructs[0].seq

def test_upper_stem_insertion():
    import pytest

    with pytest.raises(ValueError): from_name('us(5)')

    assert from_name('us(4)').seq == from_name('us(4,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAAUACCAGCCGAAAGGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(2)').seq == from_name('us(2,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCAUACCAGCCGAAAGGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0)').seq == from_name('us(0,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,7)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAUAUACCAGCCGAAAGGCCCUUGGCAGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,7)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCUGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,0,7)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCUUUCCCUGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_lower_stem_insertion():
    import pytest

    with pytest.raises(ValueError): from_name('us(7)')

    assert from_name('ls(6,0)') == from_name('ls(6)') == 'GGGGCCACTAGGGACAGGATGUUUUAAUACCAGCCGAAAGGCCCUUGGCAGUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(5,0)') == from_name('ls(5)') == 'GGGGCCACTAGGGACAGGATGUUUUAUACCAGCCGAAAGGCCCUUGGCAGAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,0)') == from_name('ls(0)') == 'GGGGCCACTAGGGACAGGATAUACCAGCCGAAAGGCCCUUGGCAGAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(6,1)') == 'GGGGCCACTAGGGACAGGATGUUUUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(6,7)') == 'GGGGCCACTAGGGACAGGATGUUUUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,1)') == 'GGGGCCACTAGGGACAGGATUAUACCAGCCGAAAGGCCCUUGGCAGUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('ls(0,7)') == 'GGGGCCACTAGGGACAGGATUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_nexus_insertion():
    assert from_name('nx(0)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nx(1)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGUAUACCAGCCGAAAGGCCCUUGGCAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nx(6)') == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGUUUUUUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_nexus_insertion_2():
    import pytest

    with pytest.raises(ValueError): from_name('nxx(5,0)')
    with pytest.raises(ValueError): from_name('nxx(0,6)')
    with pytest.raises(ValueError): from_name('nxx(0,0,4)')
    with pytest.raises(ValueError): from_name('nxx(0,0,5,0)')

    assert from_name('nxx(0,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAAUACCAGCCGAAAGGCCCUUGGCAGGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(1,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGAUACCAGCCGAAAGGCCCUUGGCAGCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(2,2)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(2,3)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGAUACCAGCCGAAAGGCCCUUGGCAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,5)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,6)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,7)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCUGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,8)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCUUUCCCUUGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,0,2)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,0,3)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCAUACCAGCCGAAAGGCCCUUGGCAGGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('nxx(4,5,10,2)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAUACCAGCCAUACCAGCCUUUCCCUUUCGGCCCUUGGCAGGGCCCUUGGCAGAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_hairpin_replacement():
    assert from_name('hp(0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(18)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(33)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(39)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(49)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCUUUCCCUUUCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'

def test_induced_dimerization():
    import pytest

    with pytest.raises(ValueError): from_name('id(0,0)')
    with pytest.raises(ValueError): from_name('id(hello,0)')
    with pytest.raises(ValueError): from_name('id(3,5)')
    with pytest.raises(ValueError): from_name('id(3,hello)')

    assert from_name('id(5,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCC'
    assert from_name('id(5,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGAUACCAGCC'
    assert from_name('id(5,2)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCAUACCAGCC'
    assert from_name('id(5,3)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUACCAGCC'
    assert from_name('id(5,4)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAAUACCAGCC'

    assert from_name('id(3,0)').seq == 'GGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,1)').seq == 'GGCCCUUGGCAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,2)').seq == 'GGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,3)').seq == 'GGCCCUUGGCAGAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('id(3,4)').seq == 'GGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'


if __name__ == '__main__':
    import sys, pytest
    pytest.main(sys.argv)
