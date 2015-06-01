#!/usr/bin/env python3

import nonstdlib

class Construct:

    def __init__(self, sequence='', tag=None, name='', constraints=''):
        self.name = name
        self._sequence = sequence

        if isinstance(tag, dict):
            self._tags = tag
        else:
            self._tags = {i: tag for i in range(len(self))}

        if constraints:
            self._constraints = constraints
        else:
            self._constraints = '.' * len(sequence)

        if len(self.constraints) != len(self.seq):
            raise ValueError("constraints don't match sequence")

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return 'Construct({})'.format(self._sequence)

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

    def show(self, style=None, start=None, end=None, pad=True, labels=True, dna=False, rev_com=False, color='auto'):

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

    def append_with_spacer(self, construct):
        self.insert_with_spacer(construct, len(self))
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

    def pad(self, length, pattern='UUUCCC'):
        self.insert(spacer(length, pattern), 0)
        self.insert(spacer(length, pattern), len(self))
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
        sgrna += Construct('GGAACUUUCAGUUUAGCGGUCU', target)
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

def theophylline_aptamer(piece='whole'):
    pieces = 'AUACCAGCC', 'GAAA', 'GGCCCUUGGCAG'
    struct = '(((((.((('  '....'  ')))....)))))'

    if piece == 'whole':
        aptamer = Construct(''.join(pieces), 'aptamer', constraints=struct)
    elif str(piece) == '5':
        aptamer = Construct(pieces[0], 'aptamer')
    elif str(piece) == '3':
        aptamer = Construct(pieces[2], 'aptamer')
    elif piece == 'linker':
        aptamer = Construct(pieces[1], 'aptamer')
    else:
        raise ValueError("must request 'whole', '5', '3', or 'linker' piece of aptamer, not {}.".format(piece))

    aptamer.name = "theophylline"
    return aptamer

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

def spacer(length, pattern='UUUCCC'):
    sequence = pattern * (1 + length // len(pattern))
    return Construct(sequence[:length])

def upper_stem_insertion(location, spacer_len=0):
    """
    Insert the aptamer into the upper stem region of the sgRNA.

    The upper stem region of the sgRNA is very tolerant to mutation.  In the 
    natural CRISPR/Cas system, this stem is actually where the two strands of  
    guide RNA (crRNA and tracrRNA) come together.

    Parameters
    ----------
    location: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.  The aptamer will be inserted 
        between the two ends of the stem.

    spacer_len: int
        Indicate how many base pairs should separate the aptamer from the upper 
        stem.  The spacer sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    if not 0 <= location <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(location))

    name = 'us({},{})'.format(location, spacer_len)
    insert_begin = 28 + location
    insert_end = 40 - location

    return make_insertion(name, insert_begin, insert_end, spacer_len)

def lower_stem_insertion(location, spacer_len=0):
    """
    Insert the aptamer into the lower stem region of the sgRNA.

    Parameters
    ----------
    location: int
        Indicate how many of the 6 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 6, although in practice I only 
        expect to use values greater than 4 or 5.  Shorter than that and you'll 
        almost certainly interfere with normal Cas9 binding.

    spacer_len: int
        Indicate how many base pairs should separate the aptamer from the upper 
        stem.  The spacer sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    if not 0 <= location <= 6:
        raise ValueError("Location for lower stem insertion must be between 0 and 6, not {}.".format(location))

    name = 'ls({},{})'.format(location, spacer_len)
    insert_begin = 20 + location
    insert_end = 50 - location

    return make_insertion(name, insert_begin, insert_end, spacer_len)

def nexus_insertion(spacer_len=0):
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
    spacer_len: int
        Indicate how many base pairs should separate the aptamer from the nexus 
        region stem.  The spacer sequence will have a UUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    Returns
    -------
    sgRNA: Construct
    """

    name = 'nx({})'.format(spacer_len)
    return make_insertion(name, 54, 59, spacer_len, 'U')
    
def hairpin_replacement(location):
    """
    Remove a portion of the 3' terminal hairpins and replace it with the 
    aptamer.
    
    Parameters
    ----------
    location: int
        Indicate how much of the 3' terminal hairpins should be kept, with the 
        counting starting at position 63.  A location of 33 therefore specifies 
        that the whole sgRNA should be kept (excluding the poly-U tail) and 
        that the aptamer should simply be added onto the end.  Values larger 
        than 33 specify that a spacer should be inserted between the sgRNA and 
        the aptamer.  Values smaller than 33 specify that some residues should 
        be truncated from the 3' end of the sgRNA.  The expected range for this 
        parameter is roughly 17-33.

    Returns
    -------
    sgRNA: Construct
        The specified construct will be returned, with a hexa-uracil tail will 
        added to the end for the benefit of the T7 polymerase.
    """

    # Remove the UUUUUU tail from the wildtype sgRNA.  This tail will be added 
    # back, in a UUUCCC pattern to avoid too many consecutive uracils, if the 
    # location is past the end of the sgRNA proper.

    design = Construct(name='hp({})'.format(location))
    design += wt_sgrna().delete(-6, ...)

    insertion_site = 63 + location

    if insertion_site < len(design):
        design.delete(insertion_site, ...)

    if insertion_site > len(design):
        design += spacer(insertion_site - len(design))

    design += theophylline_aptamer()
    design += Construct('UUUUUU')

    return design

def induced_dimerization(half, location):
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

    location: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.

    Returns
    -------
    sgRNA: Construct
    """

    # Make sure the arguments make sense.

    half = str(half)
    location = int(location)

    if not 0 <= location <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(location))

    # Construct and return the requested sequence.

    design = Construct(name='id({},{})'.format(half, location))

    if half == '5':
        design += wt_sgrna().delete(start=28+location)
        design += theophylline_aptamer('5')

    elif half == '3':
        design += theophylline_aptamer('3')
        design += wt_sgrna().delete(end=40-location)

    else:
        raise ValueError("Half for induced dimerization must be either 5 (for the 5' half) or 3 (for the 3' half), not '{}'.".format(half))

    return design

def make_insertion(name, insert_begin, insert_end, spacer_len, spacer_pattern='UUUCCC'):
    design = Construct(name=name)
    design += wt_sgrna()

    insert = theophylline_aptamer()
    insert.pad(spacer_len, spacer_pattern)

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
hp = hairpin_replacement
id = induced_dimerization


def test_construct_constraints():
    ins = Construct('AA', constraints='()')
    seq = 'AAAAAAAAAA'

    assert ins.constraints == '()'
    assert Construct(seq).constraints == '..........'
    assert Construct(seq).prepend(ins).constraints == '()..........'
    assert Construct(seq).append(ins).constraints == '..........()'
    assert Construct(seq).insert(ins, 5).constraints == '.....().....'
    assert Construct(seq).replace(3, 5, ins).constraints == '...().....'

def test_wt_sgrna():
    assert wt_sgrna().seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert wt_sgrna('rfp').seq == 'GGAACUUUCAGUUUAGCGGUCUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert wt_sgrna('vegfa').seq == 'GGGTGGGGGGAGTTTGCTCCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_theophylline_aptamer():
    assert theophylline_aptamer().seq == 'AUACCAGCCGAAAGGCCCUUGGCAG'

def test_spacer():
    assert spacer(1).seq == 'U'
    assert spacer(2).seq == 'UU'
    assert spacer(3).seq == 'UUU'
    assert spacer(4).seq == 'UUUC'
    assert spacer(5).seq == 'UUUCC'
    assert spacer(6).seq == 'UUUCCC'
    assert spacer(7).seq == 'UUUCCCU'

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
    with pytest.raises(TypeError): from_name('us')
    with pytest.raises(TypeError): from_name('us(0,0,0)')

    assert from_name('us(4)').seq == from_name('us(4,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAAUACCAGCCGAAAGGCCCUUGGCAGUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(2)').seq == from_name('us(2,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCAUACCAGCCGAAAGGCCCUUGGCAGGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0)').seq == from_name('us(0,0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAAUACCAGCCGAAAGGCCCUUGGCAGAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUAUACCAGCCGAAAGGCCCUUGGCAGUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(4,7)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,1)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAUAUACCAGCCGAAAGGCCCUUGGCAGUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'
    assert from_name('us(0,7)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAUUUCCCUAUACCAGCCGAAAGGCCCUUGGCAGUUUCCCUAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU'

def test_lower_stem_insertion():
    import pytest

    with pytest.raises(ValueError): from_name('us(7)')
    with pytest.raises(TypeError): from_name('us')
    with pytest.raises(TypeError): from_name('us(0,0,0)')

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

def test_hairpin_replacement():
    assert from_name('hp(0)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(18)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(33)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(39)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'
    assert from_name('hp(49)').seq == 'GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUCCCUUUCCCUUUCAUACCAGCCGAAAGGCCCUUGGCAGUUUUUU'

def test_induced_dimerization():
    import pytest

    with pytest.raises(TypeError): from_name('id')
    with pytest.raises(TypeError): from_name('id(0,0,0)')
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
