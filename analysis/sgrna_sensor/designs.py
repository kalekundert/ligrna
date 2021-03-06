#!/usr/bin/env python3
# encoding: utf-8

from .sequence import *
from .components import *
from .helpers import *

## Strategy Abbreviations
# f: fold
# z: zipper
# s: serpentine
# c: circle
# h: hammerhead
# r: randomize
# d: diversify (also 'm')
# q: sequence logo
# u: sequester uracil 59
# w: strand swap
# m: modulate
# o: obstruct
# b: buttress

## Domain Abbreviations
# u: upper stem
# l: lower stem
# b: bulge
# x: nexus
# r: ruler
# h: hairpin

## Design Abbreviations
# 11: rxb 11,1
# 30: mhf 30
# 37: mhf 37


def design(abbreviation, *legacy_abbreviations):

    def finalize_design(factory, *args, **kwargs):
        import inspect
        argspec = inspect.getargspec(factory)

        prefix_args = []
        suffix_args = []
        defaults = {}

        for i, value in enumerate(args):
            defaults_i = i - len(argspec.args) + len(argspec.defaults)
            if defaults_i < 0 or value != argspec.defaults[defaults_i]:
                if argspec.args[i] in ('species', 'target', 'ligand'):
                    defaults[argspec.args[i]] = str(value)
                    prefix_args.append(str(value))
                else:
                    suffix_args.append(str(value))

        construct = factory(*args, **kwargs)
        assert construct is not None, 'Forgot to return a construct from {}'.format(factory.__name__)
        tokens = prefix_args + [abbreviation] + suffix_args
        construct.slash_name = construct.name = '/'.join(tokens)
        construct.underscore_name = '_'.join(tokens)
        construct.comma_name = '{} {} {}'.format(' '.join(prefix_args), abbreviation, ','.join(suffix_args))
        construct.function_name = '{} {}({})'.format(' '.join(prefix_args), abbreviation, ','.join(suffix_args))
        construct.flags = prefix_args
        construct.abbrev = abbreviation
        construct.args = suffix_args
        construct.design = (abbreviation, *suffix_args)
        construct.spacer = kwargs.get('target', defaults.get('target'))
        construct.ligand = kwargs.get('ligand', defaults.get('ligand'))
        construct.species = kwargs.get('species')
        construct.doc = factory.__doc__

        return construct

    def decorator(factory):
        import decorator
        design = decorator.decorate(factory, finalize_design)
        for name in (abbreviation,) + legacy_abbreviations:
            globals()[name] = design
        return design


    return decorator


@design('wt')
def wt_sgrna(target='none'):
    """
    Return the wildtype sgRNA sequence.

    The construct is composed of 3 domains: stem, nexus, and hairpins.  The 
    stem domain encompasses the lower stem, the bulge, and the upper stem.  
    Attachments are allowed pretty much anywhere, although it would be prudent 
    to restrict this based on the structural biology of Cas9 if you're planning 
    to make random attachments.
    """
    sgrna = Construct('wt')

    sgrna += spacer(target)

    sgrna += Domain('stem', 'GUUUUAGAGCUAGAAAUAGCAAGUUAAAAU')
    sgrna += Domain('nexus', 'AAGGCUAGUCCGU')
    sgrna += Domain('hairpins', 'UAUCAACUUGAAAAAGUGGCACCGAGUCGGUGC')
    sgrna += Domain('tail', 'UUUUUU')

    sgrna['stem'].expected_fold = '((((((..((((....))))....))))))'
    sgrna['hairpins'].expected_fold = '.....((((....)))).((((((...))))))'

    sgrna['stem'].style = 'green'
    sgrna['nexus'].style = 'red'
    sgrna['hairpins'].style = 'blue'

    sgrna['stem'].attachment_sites = 'anywhere'
    sgrna['nexus'].attachment_sites = 'anywhere'
    sgrna['hairpins'].attachment_sites = 'anywhere'

    return sgrna

@design('dead')
def dead_sgrna(target='none'):
    """
    Return the sequence for the negative control sgRNA.

    This sequence has two mutations in the nexus region that prevent the sgRNA 
    from folding properly.  These mutations were described by Briner et al.
    """
    sgrna = wt_sgrna(target)
    sgrna.name = 'dead'

    sgrna['nexus'].mutable = True
    sgrna['nexus'].mutate(2, 'C')
    sgrna['nexus'].mutate(3, 'C')
    sgrna['nexus'].mutable = False

    return sgrna

@design('liu')
def liu_sgrna(target='none', ligand='theo'):
    spacer_seq = spacer(target).rna
    stem_5 = rna_reverse_complement(spacer_seq[:15])
    stem_3 = rna_reverse_complement(stem_5[-9:])

    sgrna = wt(target=target)
    sgrna.remove('tail')
    sgrna += Domain('stem/5', stem_5)
    sgrna += aptamer(ligand, liu=True)
    sgrna += Domain('stem/3', stem_3)
    sgrna += Domain('tail', 'TTTTTT')

    return sgrna

@design('on')
def on(pam=None, target='none', species='sp'):
    """
    Return an optimized sgRNA sequence.

    This is an optimized version of the standard sgRNA sequence used for 
    Cas9-mediated genome editing, gene regulation, and chromosome labeling.  
    The optimizations come from Dang et al. Genome Biology 12:280 (2015).  
    First, a base pair in the lower stem is changed from ``UA`` to ``CG`` to 
    breakup a series of 4 thymidines that stalls the mammalian RNA polymerase.
    Second, the upper stem is extended by 5 base pairs, taken from the native 
    crRNA/tracrRNA duplex (which is 10bp longer than the canonical sgRNA).

    This construct is constitutively on and is meant to be used as a positive 
    control.
    """
    sgrna = Construct('on')
    sgrna += spacer(target, species)

    # Although this sequence is just an optimized version of ``wt``, it is 
    # constructed rather differently.  
    # 
    # First of all, it has a different name.  I do think ``on`` is more clear 
    # than ``wt``, because this construct shows me what happens when Cas9 is 
    # on.  The name ``wt`` also never really made sense, because sgRNA is 
    # inherently artificial.  But my real motivation was to name the negative 
    # control something other than ``dead``.  The ``dead`` name was confusing 
    # because lots of things can be dead, and it's not always clear which ones 
    # I'm talking about.  I think ``off`` will be much more clear.
    #
    # More importantly, the domains are much more finely divided.  I've found 
    # that this makes it easier to construct designs, both because there are 
    # more places where sequences can be inserted without messing up the 
    # indexing and because you don't have to count as far to figure out 
    # insertion indices and the like.  It's never been worth the effort to 
    # update ``wt``, but I hope that what I'll lose here in interoperability 
    # I'll gain in ease-of-use.

    if species == 'sp':  # S. pyogenes
        sgrna += Domain('lower_stem/5', 'GUUUCA', 'green')
        sgrna += Domain('bulge/5', 'GA', 'yellow')
        sgrna += Domain('upper_stem/5', 'GCUAUGCUG', 'green')
        sgrna += Domain('upper_stem/o', 'GAAA', 'green')
        sgrna += Domain('upper_stem/3', 'CAGCAUAGC', 'green')
        sgrna += Domain('bulge/3', 'AAGU', 'yellow')
        sgrna += Domain('lower_stem/3', 'UGAAAU', 'green')
        sgrna += Domain('nexus/aa', 'AA', 'red')
        sgrna += Domain('nexus/5', 'GG', 'red')
        sgrna += Domain('nexus/o', 'CUAGU', 'red')
        sgrna += Domain('nexus/3', 'CC', 'red')
        sgrna += Domain('ruler', 'GUUAUCA', 'magenta')
        sgrna += Domain('hairpin/5', 'ACUU', 'blue')
        sgrna += Domain('hairpin/o', 'GAAA', 'blue')
        sgrna += Domain('hairpin/3', 'AAGU', 'blue')
        sgrna += Domain('terminator/5', 'GGCACCG', 'blue')
        sgrna += Domain('terminator/o', 'AGU', 'blue')
        sgrna += Domain('terminator/3', 'CGGUGC', 'blue')
        sgrna += Domain('terminator/u', 'UUUUUU', 'blue')

        if pam == 'pam':
            sgrna['lower_stem/5'][1:3] = 'GG'
            sgrna['lower_stem/3'][3:5] = 'CC'

    elif species == 'sa':  # S. aureus
        sgrna += Domain('lower_stem/5', 'GUUUUAGUA', 'green')
        sgrna += Domain('bulge/5', 'C', 'yellow')
        sgrna += Domain('upper_stem/5', 'UCUG', 'green')
        sgrna += Domain('upper_stem/o', 'GAAA', 'green')
        sgrna += Domain('upper_stem/3', 'CAGA', 'green')
        sgrna += Domain('bulge/3', 'AUC', 'yellow')
        sgrna += Domain('lower_stem/3', 'UACUAAAAC', 'green')
        sgrna += Domain('nexus/aa', 'AA', 'red')
        sgrna += Domain('nexus/g', 'G', 'red')  # Setup the scaffold so the 
        sgrna += Domain('nexus/5', 'GC', 'red') # nexus stem is still 2 bp.
        sgrna += Domain('nexus/o', 'AAAAU', 'red')
        sgrna += Domain('nexus/3', 'GC', 'red')
        sgrna += Domain('nexus/c', 'C', 'red')
        sgrna += Domain('ruler', 'GUGUUU', 'magenta')
        sgrna += Domain('hairpin/5', 'AUCUCGUCAA', 'blue')
        sgrna += Domain('hairpin/o', 'CUUG', 'blue')
        sgrna += Domain('hairpin/3', 'UUGGCGAGAU', 'blue')
        sgrna += Domain('terminator/5', '', 'blue')
        sgrna += Domain('terminator/o', '', 'blue')
        sgrna += Domain('terminator/3', '', 'blue')
        sgrna += Domain('terminator/u', 'UUUUUUU', 'blue')

    # This is a hybrid sgRNA scaffold where the nexus comes from S. pyogenes 
    # and everything else comes from S. aureus.  I don't have any evidence that 
    # this scaffold actually works, but I made it because I think it might have 
    # a better chance of accommodating the ligRNAs.
    elif species == 'sap':
        sgrna += Domain('lower_stem/5', 'GUUUUAGUA', 'green')
        sgrna += Domain('bulge/5', 'C', 'yellow')
        sgrna += Domain('upper_stem/5', 'UCUG', 'green')
        sgrna += Domain('upper_stem/o', 'GAAA', 'green')
        sgrna += Domain('upper_stem/3', 'CAGA', 'green')
        sgrna += Domain('bulge/3', 'AUC', 'yellow')
        sgrna += Domain('lower_stem/3', 'UACUAAAAC', 'green')
        sgrna += Domain('nexus/aa', 'AA', 'red')
        sgrna += Domain('nexus/5', 'GG', 'red')
        sgrna += Domain('nexus/o', 'CUAGU', 'red')
        sgrna += Domain('nexus/3', 'CC', 'red')
        sgrna += Domain('ruler', 'GUGUUU', 'magenta')
        sgrna += Domain('hairpin/5', 'AUCUCGUCAA', 'blue')
        sgrna += Domain('hairpin/o', 'CUUG', 'blue')
        sgrna += Domain('hairpin/3', 'UUGGCGAGAU', 'blue')
        sgrna += Domain('terminator/5', '', 'blue')
        sgrna += Domain('terminator/o', '', 'blue')
        sgrna += Domain('terminator/3', '', 'blue')
        sgrna += Domain('terminator/u', 'UUUUUUU', 'blue')

    else:
        raise ValueError('Unknown species: %s' % species)

    return sgrna

@design('off')
def off(pam=None, target='none', species='sp'):
    """
    Return the sequence for the negative control sgRNA.

    This sequence has two mutations in the nexus region that prevent the sgRNA 
    from folding properly.  These mutations were described by Briner et al.

    I don't know a priori that the negative control will work with SaCas9.
    """
    sgrna = on(pam=pam, target=target, species=species)
    sgrna.name = 'off'

    sgrna['nexus/5'].seq = 'C' * len(sgrna['nexus/5'])
    sgrna['nexus/3'].seq = 'C' * len(sgrna['nexus/3'])

    if species == 'sa':
        sgrna['nexus/g'].seq = 'C' * len(sgrna['nexus/g'])


    return sgrna

@design('fu', 'us')
def fold_upper_stem(N, linker_len=0, splitter_len=0, num_aptamers=1, target='none', ligand='theo'):
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
        Indicate how many bases should separate the aptamer from the upper 
        stem.  The linker sequence will have a UUUCCCUUUCCC... pattern so that 
        the design doesn't have really long repeats or an out-of-whack GC%.

    splitter_len: int
        Indicate how many bases should separate the 3' half of the aptamer from 
        the 5' half.  The splitter sequence will have the same pattern as the 
        linker (see above).

    num_aptamers: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.
    """

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    if num_aptamers != 1:
        args = N, linker_len, splitter_len, num_aptamers
    elif splitter_len != 0:
        args = N, linker_len, splitter_len
    else:
        args = N, linker_len

    sgrna = wt_sgrna(target)
    sgrna.attach(
            aptamer_insert(
                ligand,
                linker_len=linker_len,
                splitter_len=splitter_len,
                num_aptamers=num_aptamers,
            ),
            'stem', 8 + N,
            'stem', 20 - N,
    )
    return sgrna

@design('fl', 'ls')
def fold_lower_stem(N, linker_len=0, splitter_len=0, target='none', ligand='theo'):
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

    splitter_len: int
        Indicate how many bases should separate the 3' half of the aptamer from 
        the 5' half.  The splitter sequence will have the same pattern as the 
        linker (see above).
    """

    if not 0 <= N <= 6:
        raise ValueError("Location for lower stem insertion must be between 0 and 6, not {}.".format(N))

    if splitter_len != 0:
        args = N, linker_len, splitter_len
    else:
        args = N, linker_len

    sgrna = wt_sgrna(target)
    sgrna.attach(
            aptamer_insert(
                ligand,
                linker_len=linker_len,
                splitter_len=splitter_len,
            ),
            'stem', 0 + N,
            'stem', 30 - N,
    )
    return sgrna

@design('fx', 'nx')
def fold_nexus(linker_len=0, target='none', ligand='theo'):
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
    """

    sgrna = wt_sgrna(target)
    sgrna.attach(
            aptamer_insert(
                ligand,
                linker_len=linker_len,
                repeat_factory=lambda name, length, end: repeat(name, length, end, 'U'),
            ),
            'nexus', 4,
            'nexus', 9,
    )
    return sgrna
    
@design('fxv', 'nxx')
def fold_nexus_2(N, M, splitter_len=0, num_aptamers=1, target='none', ligand='theo'):
    """
    Insert the aptamer into the nexus region of the sgRNA.

    This design strategy expands upon the original fold_nexus() function, 
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

    splitter_len: int
        The number of base pairs to insert into the middle of the aptamer.  The 
        linker will have the sequence 'UCGUCG...', which was chosen because it 
        has very low complementarity with the rest of the design.

    num_aptamers: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.
    """

    # Make sure the arguments have reasonable values.

    min_splitter_len = len(aptamer('theo', 'splitter'))

    if not 0 <= N <= 4:
        raise ValueError("nxx: N must be between 0 and 4, not {}".format(N))
    if not 0 <= M <= 5:
        raise ValueError("nxx: M must be between 0 and 5, not {}".format(N))
    if 0 < splitter_len <= min_splitter_len:
        raise ValueError("nxx: splitter_len must be longer than {} (the natural linker length).".format(min_splitter_len))
    if num_aptamers < 1:
        raise ValueError("nxx: Must have at least 1 aptamer")

    # Figure out what to name the construct.  Make an effort to exclude 
    # arguments that the user didn't actually specify from the name.

    if num_aptamers != 1:
        args = N, M, splitter_len, num_aptamers
    elif splitter_len != 0:
        args = N, M, splitter_len
    else:
        args = N, M

    # Create and return the construct using a helper function.

    sgrna = wt_sgrna(target)
    sgrna.attach(
            aptamer_insert(
                ligand,
                splitter_len=splitter_len,
                num_aptamers=num_aptamers,
            ),
            'nexus', 2 + N,
            'nexus', 11 - M,
    )
    return sgrna

@design('fh')
def fold_hairpin(H, N, A=1, target='none', ligand='theo'):
    """
    Replace either of the hairpins with the aptamer.  Briner et al. showed that 
    the sgRNA is at least somewhat sensitive to the distance between the nexus 
    and the hairpins, so unfolding the first hairpin may be a successful way to 
    create a sensor.  They also showed that the sgRNA is very sensitive to the 
    removal of both hairpins, but not so much to the removal of just the first.  
    They didn't try removing just the second, but it's not unreasonable to 
    think that that might be a viable way to control the sgRNA.  

    Briner et al. also didn't try changing the sequence of either hairpins, so 
    I'm just assuming that they can be freely changed as long as the base 
    pairing is maintained.  In the crystal structure, the first hairpin is not 
    interacting with Cas9 at all and the second hairpin is unresolved, so I 
    think this assumption is reasonable.  It's also worth noting that the first 
    hairpin is solvent exposed, so it should be able to sterically accommodate 
    the aptamer.

    Parameters
    ----------
    H: int
        Which hairpin to replace.  Must be either 1 or 2.  Replacing the second 
        hairpin may not be a good idea, because it think it's part of the T7 
        terminator, but I can still test it in vitro.  Worst case is that it 
        won't work as expected in vivo.

    N: int
        Indicate how many of the wildtype base pairs should be preserved.  
        This parameters must be between 0 and the number of wildtype base 
        pairs, which is 4 for the first hairpin and 6 for the second.  The 
        aptamer will be inserted between the two ends of the stem.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    ligand: str
        Which aptamer to insert into the sgRNA.  Must be one of the strings 
        accepted by the aptamer() function.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    if H not in (1, 2):
        raise ValueError("fh(H,N): H must be either 1 or 2")

    max_N = (4 if H == 1 else 6)
    if not 0 <= N <= max_N:
        raise ValueError("fh(H,N): N must be between 0 and {}".format(max_N))

    sgrna = wt_sgrna(target)
    sgrna.attach(
            aptamer_insert(ligand, num_aptamers=A),
            'hairpins',  5 + N if H == 1 else 18 + N,
            'hairpins', 17 - N if H == 1 else 33 - N,
    )
    return sgrna

@design('hp')
def replace_hairpins(N, target='none', ligand='theo'):
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
    design = wt_sgrna(target)

    domain_len = len(design['hairpins'])
    insertion_site = min(N, domain_len)
    linker_len = max(0, N - domain_len), 0

    design.attach(
            aptamer_insert(ligand, linker_len=linker_len),
            'hairpins', insertion_site,
            'hairpins', '...',
    )
    return design

@design('zu', 'id')
def zipper_upper_stem(half, N, target='none', ligand='theo'):
    """
    Split the guide RNA into its two naturally occurring halves, and use the 
    aptamer to bring those halves together in the presence of the ligand.  This 
    is known as the "zipper" strategy, because the two strands of RNA will be 
    "zipped" together by the ligand.  The aptamer replaces some or all of the 
    upper stem.  We have already observed that an sgRNA with the upper stem 
    fully replaced by the theophylline aptamer is fully functional, so the 
    design should work if the ligand successfully induces dimerization.

    Parameters
    ----------
    half: 5 or 3
        Indicate which half of the split construct to return.  '5' and '3' 
        refer to the 5' and 3' halves, respectively.

    N: int
        Indicate how many of the 4 upper stem base pairs should be preserved.  
        This parameters must be between 0 and 4.
    """

    # Make sure the arguments make sense.

    half = str(half)
    N = int(N)

    if not 0 <= N <= 4:
        raise ValueError("Location for upper stem insertion must be between 0 and 4, not {}.".format(N))

    # Construct and return the requested sequence.

    design = Construct()
    wt = wt_sgrna(target)

    if half == '5':
        try: design += wt['spacer']
        except KeyError: pass
        design += wt['stem']
        design.attach(
                aptamer(ligand, '5'),
                'stem', 8 + N, 'stem', '...',
        )
    elif half == '3':
        design += wt
        design.attach(
                aptamer(ligand, '3'),
                'stem', '...', 'stem', 20 - N,
        )
    else:
        raise ValueError("Half for induced dimerization must be either 5 (for the 5' half) or 3 (for the 3' half), not '{}'.".format(half))

    return design

@design('sb')
def serpentine_bulge(N, tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Sequester the bulge in a non-productive hairpin when the ligand isn't 
    present.  The bulge is an interesting target because it doesn't have to be 
    there, but if it is there it must be unpaired and it must have its wildtype 
    sequence.  This design uses the two adenosines that are naturally in the 
    bulge to construct a tetraloop that caps the non-productive hairpin.  Below 
    is an ASCII-art schematic of the design, along with an example sequence:

       ┌──────────┐┌───────────┐┌────┐┌────────────┐┌─────┐┌──────────┐ 
    5'─┤lower stem├┤  bulge''  ├┤theo├┤   bulge'   ├┤bulge├┤lower stem├─3'
       └──────────┘└───────────┘└────┘└────────────┘└─────┘└──────────┘ 
        GUUUUAga    UCGU(UAAAAU) ...  (GUUUUA)AC-GA  AA-GU  UAAAAU
                                                 └────┘
                                                tetraloop

    The length of the non-productive hairpin can be extended by including bases 
    from the lower stem, as shown in parentheses.  Mutations can be made in the 
    bulge', bulge'', and lower stem regions to tune the balance between the 
    "on" and "off" states.  The bulge itself is never changed.

    Parameters
    ----------
    N: int
        Indicate how long the non-productive hairpin should be.  It can't be 
        shorter than 2 base pairs.  The first two bases in the hairpin come 
        from the bulge, and subsequent bases come from the lower stem.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    if N < 2:
        raise ValueError("sb(N): N must be 2 or greater")

    sgrna = wt_sgrna(target)
    sgrna.attach(
            serpentine_insert(
                ligand,
                wt_sgrna()['stem'][22:22+N], '3',
                tuning_strategy, num_aptamers=A,
            ),
            'stem', 8,
            'stem', 22,
    )
    sgrna['on'].prepend('UC')

    return sgrna

@design('sl')
def serpentine_lower_stem(tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Sequester the nexus in base pairs with the lower stem in the absence of the 
    ligand.  This design is based off two ideas:
    
    1. That disrupting the nexus will be an effective way to deactivate the 
       sgRNA, because the nexus seems to be very sensitive to mutation.

    2. That the lower stem can be modified to have some complementarity with 
       the nexus, because the exact sequence of the lower stem seems to be 
       unimportant, so long as it does actually form a stem.
    
    This design is named "serpentine_lower_stem" because it uses applies the 
    "serpentine" strategy to the lower stem region of the sgRNA.  A schematic 
    of this strategy is shown below.  The "serpentine" pattern is formed 
    because nexus' can base pair either with nexus or nexus''.  Note that the 
    length of the serpentine pattern is fixed at four base pairs, because the 
    length of the lower stem must be six base pairs (and two base pairs are 
    required to form the tetraloop).

       ┌───────┐┌──┐┌────┐┌────┐┌──────┐┌───────┐ 
    5'─┤nexus''├┤GA├┤theo├┤AAGU├┤nexus'├┤ nexus ├─3'
       └───────┘└──┘└────┘└────┘└──────┘└───────┘ 
        UC-GGCU  GA  ...   AAGU  AGCC-GA AA-GGCU
                                      └───┘
                                    tetraloop
    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            serpentine_insert(
                ligand,
                'GGCU', '3',
                tuning_strategy,
                num_aptamers=A,
            ),
            'stem', 0,
            'nexus', 2,
    )
    sgrna['on'].prepend('UC')
    sgrna['on'].append('GA')
    sgrna['switch'].prepend('AAGU')
    return sgrna

@design('slx')
def serpentine_lower_stem_around_nexus(tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Use the lower stem to extend the nexus stem in the absence of the aptamer 
    ligand.  This design is based of the idea that the sgRNA is very sensitive 
    to the length of the nexus stem and that the bases in the lower stem can be 
    freely mutated to complement the region just beyond the nexus stem.  The 
    extended stem will have a bulge because there is a short AA linker between 
    the lower stem and the nexus, and the length of the complementary region 
    will be fixed at 6 base pairs because the lower stem cannot be lengthened 
    or shortened.  A schematic of this design is shown below:

       ┌──────┐┌──┐┌────┐┌────┐┌──────┐┌──┐┌─────────┐┌──────┐ 
    5'─┤  on  ├┤GA├┤theo├┤AAGU├┤switch├┤AA├┤  nexus  ├┤ off  ├─3'
       └──────┘└──┘└────┘└────┘└──────┘└──┘└─────────┘└──────┘ 
        GUUAUC  GA  ...   AAGU  GAUAAC  AA  GGCUAGUCC  GUUAUC
    
    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            serpentine_insert(
                ligand,
                'GUUAUC', '3',
                tuning_strategy,
                turn_seq='',
                num_aptamers=A,
            ),
            'stem', '...',
            'stem', '...',
    )
    sgrna['on'].append('GA')
    sgrna['switch'].prepend('AAGU')
    return sgrna

@design('sh')
def serpentine_hairpin(N, tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Sequester the 3' end of the nexus in base pairs with the 5' strand of the 
    first hairpin in the absence of aptamer ligand.  This design is based on 
    the fact that proper nexus folding is required for sgRNA function and the 
    assumption that the sequence of the first hairpin can be changed if its 
    base pairing is maintained.  Briner et al. didn't actually test any point
    mutations in the first hairpin, but they did find that the whole hairpin 
    can be deleted so long as a two residue spacer is added to maintain the 
    positioning of the second hairpin.

       ┌────────────┐┌────┐┌──────┐┌────┐┌───────┐ 
    5'─┤   nexus    ├┤turn├┤nexus'├┤theo├┤nexus''├─3'
       └────────────┘└────┘└──────┘└────┘└───────┘ 
        GGCUAGUCCGUU  AUCA  AACG... ...   ...CGUU
    
    Parameters
    ----------
    N: int
        The length of the complementary region to insert, and also the length 
        of the first hairpin.  The hairpin is naturally 4 base pairs long, but 
        it's solvent exposed so in theory you can make it as long as you want.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    if not 4 <= N <= 14:
        raise ValueError("sh(N): N must be between 4 and 14")

    sgrna = wt_sgrna(target)
    sgrna.attach(
            serpentine_insert(
                ligand,
                wt_sgrna().seq[44-N:44], '5',
                tuning_strategy,
                turn_seq='AUCA', # ANYA
                num_aptamers=A,
            ),
            'hairpins', 1,
            'hairpins', 17,
    )
    return sgrna

@design('cb')
def circle_bulge(tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Extend the lower stem hairpin through the bulge when the small molecule is 
    absent.  This design is based off the fact that "straightening" the bulge 
    (i.e. mutating both side so they can base pair) completely eliminates Cas9 
    activity.  Note that this design unconditionally removes the 5' part of the 
    bulge, which has the sequence 'GA'.  In wildtype sgRNA, this mutation does
    not have a significant effect.  

    This design is named "circle_bulge" because it uses the "circle" strategy 
    to sequester the bulge region of the sgRNA.  A schematic of this strategy 
    is shown below.  The circle is formed when bulge' binds to either bulge'' 
    or bulge.  The sgRNA is only active when bulge is unpaired, and ligand 
    binding by the aptamer should encourage this conformation.

       ┌──────────┐┌──────┐┌────┐┌───────┐┌─────┐┌──────────┐ 
    5'─┤lower stem├┤bulge'├┤theo├┤bulge''├┤bulge├┤lower stem├─3'
       └──────────┘└──────┘└────┘└───────┘└─────┘└──────────┘ 
        GUUUUA      ACUU    ...   AAGU     AAGU   UAAAAU

    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            circle_insert(
                ligand, 'AAGU', '3',
                tuning_strategy, num_aptamers=A,
            ),
            'stem', 6,
            'stem', 20,
    )
    return sgrna

@design('cbc')
def circle_bulge_combo(tuning_strategy, combo_strategy, combo_arg=None, A=1, target='none', ligand='theo'):
    """
    Combine the circle bulge design with orthogonal designs.  The idea is to 
    increase fold activation, possibly at the expense of affinity, by requiring 
    two switches to turn on.  Only a select set of orthogonal designs, known to 
    be functional on their own, can be combined with 'cb'.  This set includes 
    most of the 'slx' and 'sh' families of designs.

    Parameters
    ----------
    tuning_strategy: str
        A string specifying which mutation(s) to make in the 'cb' switch.

    combo_strategy: str
        A string specifying which design to integrate into 'cb'. Either 'slx' 
        or 'sh'.
        
    combo_arg:
        Arguments to the orthogonal design.  What's expected depends on the 
        value of 'combo_strategy'.
    """
    sgrna = circle_bulge(tuning_strategy)

    # Serpentine the lower stem around the nexus.  This code isn't done by 
    # making an attachment, like all the other designs are, because its 
    # attachment would overlap with circle bulge.  Instead, the on and switch 
    # domains are directly mutated into the existing stem domain.

    if combo_strategy == 'slx':
        L = len(sgrna['stem'])
        switch_domain, on_domain, off_domain = tunable_switch(
                'GUUAUC', combo_arg or 'wo')
        sgrna['stem'].replace(0, 6, on_domain.seq)
        sgrna['stem'].replace(L-6, L, switch_domain.seq)

    # Serpentine the first hairpin.  This code is copied verbatim from the sh() 
    # function.

    elif combo_strategy == 'sh':
        if combo_arg is None:
            raise ValueError("The 'sh' combo strategy requires an argument.")
        sgrna.attach(
                serpentine_insert(
                    ligand,
                    wt_sgrna().seq[44-combo_arg:44], '5',
                    '',
                    turn_seq='AUCA', # ANYA
                    num_aptamers=A,
                ),
                'hairpins', 1,
                'hairpins', 17,
        )
    else:
        raise ValueError("unsupported strategy: '{}'".format(strategy))

    return sgrna

@design('cl')
def circle_lower_stem(tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Sequester the 5' half of the nexus in base pairs with the 5' half of the 
    lower stem in the absence of aptamer ligand.  This strategy is based on  
    the fact that the nexus must be natively folded for the sgRNA to function 
    and that the specific sequence in the lower stem doesn't matter as long as 
    it's well base paired.

    This is an application of the "circle" strategy, which is known as "strand 
    displacement" in the literature.  The 5' half of the lower stem (nexus') 
    can either base pair with the 3' half of the lower stem (nexus'') or the 5' 
    half of the nexus.  The former is the active state and the latter is the 
    inactive state.  When the aptamer binds its ligand, that should encourage 
    the formation of the active state.  A schematic of the design strategy is 
    shown below:

       ┌──────┐┌──┐┌────┐┌────┐┌───────┐┌─────┐ 
    5'─┤nexus'├┤AG├┤theo├┤AAGU├┤nexus''├┤nexus├─3'
       └──────┘└──┘└────┘└────┘└───────┘└─────┘ 
        AGCCUU  AG  ...   AAGU  AAGGCU   AAGGCU 

    Note that the length of the nexus' and nexus'' sequences must be six, 
    because the length of the lower stem cannot change.  Currently, the 
    sequence is also fixed to match the start of the nexus (AAGGCU), but this 
    doesn't have to be the case.  Sliding this sequence in the 3' direction 
    could also yield viable designs.

    Parameters
    ----------
    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            circle_insert(
                ligand, 'AAGGCU', '3',
                tuning_strategy, num_aptamers=A,
            ),
            'stem', 0,
            'stem', '...',
    )
    sgrna['switch'].append('GA')
    sgrna['on'].prepend('AAGU')
    return sgrna

@design('ch')
def circle_hairpin(N, tuning_strategy='', A=1, target='none', ligand='theo'):
    """
    Move the nexus closer to the hairpins in the absence of the aptamer's 
    ligand.  This design is supported by the fact that inserting one residue 
    into the region between the nexus and the hairpins substantially reduces 
    sgRNA function.  Briner et al. didn't try to remove residues from this 
    region, but it seems reasonable to expect that doing so would also be 
    quite deleterious.
    
    This is an application of the "circle" strategy, which is known as "strand 
    displacement" in the literature.  The 5' half of the first hairpin (ruler') 
    can either base pair with the 3' half of the same hairpin (ruler'') or the 
    region between the nexus and the hairpin (ruler).  The former is the 
    active state and the latter is the inactive state.  When the aptamer binds 
    its ligand, that should encourage the formation of the active state.  A 
    schematic of the design strategy is shown below:

       ┌──────┐┌───────┐┌────┐┌──────┐ 
    5'─┤ruler ├┤ruler''├┤theo├┤ruler'├─3'
       └──────┘└───────┘└────┘└──────┘ 
        ..AUCA  ..AUCA   ...   UGAU..  

    Parameters
    ----------
    N: int
        The length of the complementary region to insert, and also the length 
        of the first hairpin.  The hairpin is naturally 4 base pairs long, but 
        it's solvent exposed so in theory you can make it as long as you want.

    A: int
        The number of aptamers to insert into the sgRNA.  The aptamers are 
        inserted within each other, in a manner than should give rise to 
        positive cooperativity.

    target: str
        The name of the sequence the sgRNA should target, or None if you just 
        want the sgRNA without any spacer sequence at all.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            circle_insert(
                ligand,
                wt_sgrna().seq[48-N:48], '5',
                tuning_strategy,
                num_aptamers=A),
            'hairpins', 5,
            'hairpins', 17,
    )
    return sgrna

@design('hu')
def hammerhead_upper_stem(mode, A=1, target='none', ligand='theo'):
    sgrna = wt_sgrna(target)
    sgrna.attach(
            hammerhead_insert(ligand, mode, num_aptamers=A),
            'stem', 8,
            'stem', 20,
    )
    return sgrna

@design('hx')
def hammerhead_nexus(mode, A=1, target='none', ligand='theo'):
    sgrna = wt_sgrna(target)
    sgrna.attach(
            hammerhead_insert(ligand, mode, num_aptamers=A),
            'nexus', 2,
            'nexus', 11,
    )
    return sgrna

@design('hh')
def hammerhead_hairpin(mode, A=1, target='none', ligand='theo'):
    sgrna = wt_sgrna(target)
    sgrna.attach(
            hammerhead_insert(ligand, mode, num_aptamers=A),
            'hairpins', 5,
            'hairpins', 17,
    )
    return sgrna

@design('rb')
def randomize_bulge(N, M, flags='', A=1, target='none', ligand='theo'):
    sgrna = wt_sgrna(target)
    sgrna.attach(
            random_insert(ligand, N, M, flags),
            'stem', 6,
            'stem', 24,
    )
    return sgrna

@design('rbi')
def randomize_bulge_i(N, M, bp='G', target='none', ligand='theo'):
    """
    Replace the upper stem with the aptamer and randomize the bulge to connect 
    it to the lower stem.

    This is a variant of the rb library with two small differences.  First, the 
    nucleotides flanking the aptamer are not randomized and are instead 
    guaranteed to base pair.  The default base pair is GC.  However, note that 
    to be consistent with rb, this base pair is considered part of the linker, 
    and is included in the N and M arguments.  So rbi/4/8 only randomizes 10 
    positions.  Second, the library is based off the Dang scaffold.  Most 
    extended upper stem is replaced with the aptamer, but the CG base pair in 
    the lower stem remains.

    Parameters
    ----------
    N: int
        The length of the linker on the 5' side of the aptamer.  This length 
        includes a non-randomized base pair immediately adjacent to the aptamer.

    M: int
        The length of the linker on the 3' side of the aptamer.  This length 
        includes a non-randomized base pair immediately adjacent to the aptamer.

    bp: 'ACGU'
        Not implemented, but this would be a good interface for changing the 
        static base pair.  Right now to base pair is hard-coded to be GC.
    """
    sgrna = on(target=target)
    sgrna['bulge/5'].attachment_sites = 0,
    sgrna['bulge/3'].attachment_sites = 4,
    sgrna.attach(
            random_insert(ligand, N, M, flags='g'),
            'bulge/5', 0,
            'bulge/3', 4,
    )
    return sgrna

@design('rbf')
def randomize_bulge_forward(i, target='none', ligand='theo'):
    """
    rbf(6):
        The 5' link can base pair with the aptamer and the 3' linker can base 
        pair with the nexus.  The lower stem is never predicted to form and the 
        3' linker is always predicted to base pair with the nexus.

    rbf(8):
        Predicted to work.  The linkers have weak complementarity with each 
        other.  The lower stem is predicted to be unfolded without theo (by MEA 
        but not MFE) and correctly folded with theo (by MEA and MFE).

    rbf(13):
        The 3' linker has complementarity with the nexus and the aptamer.  The 
        5' linker doesn't seem to have complementarity with anything.  The 
        whole sgRNA is predicted to change folds upon theo binding, but not 
        predicted to work in either state.

    rbf(26):
        Predicted to fold differently with and without theo, but not predicted 
        to adopt the functional fold in either state.  The linkers don't seem 
        to have any complementarity.

    rbf(39):
        The whole sgRNA is predicted to be dramatically misfolded without theo 
        (the upper stem, aptamer, and random linkers are forming a big stem 
        with the nexus and the first hairpin, with the lower stem acting as a 
        hepta-loop).  The upper and lower stems are predicted to be unfolded 
        with theo.  The linkers don't seem to have any complementarity.

    rbf(40):
        The 5' linker has complementarity with the aptamer, and the 3' linker 
        has complementarity with the nexus.  The nexus is predicted to be 
        misfolded with or without theo, but I suspect that isn't the case in 
        real life.

    rbf(47):
        The 3' linker has complementarity with the aptamer and the nexus.  It's 
        predicted to be base-paired to the aptamer with theo and to the nexus 
        without theo.  Neither state is predicted to be functional.

    rbf(50):
        The aptamer is predicted to be correctly folded with or without theo.
        The linkers both have complementarity with the nexus and are predicted 
        to base pair with it unconditionally.

    rbf(51):
        Predicted to work.  The 5' linker can base pair with the nexus and the 
        3' linker can base pair with the aptamer.  The lower stem is predicted 
        to form upon theo binding, although there's not really a bulge.

    rbf(53):
        Predicted to work.  Without theo, the 5' half of the sgRNA up through 
        the aptamer is predicted to form a big stem with everything else up to 
        the hairpin, with the 3' linker acting as a hexa-loop.  With theo, the 
        lower stem is predicted to form correctly, although the bulge is not 
        really present.  The linkers have some complementarity.

    rbf(56):
        The 3' linker has complementarity with the nexus.  The 5' linker 
        doesn't really have complementarity with anything.  The lower stem is 
        never predicted to fold.

    rbf(161):
        Predicted to work with GFP, AAVS, and null spacers.  The 3' linker can 
        base pair with the aptamer, which encourages the 5' lower stem to 
        sequester the nexus.  The 3' linker can also base pair with the 5' 
        linker (albeit less favorably: 6bp vs 4bp), forming the basis of a 
        strand displacement mechanism.
    """
    linkers = {
            6:  (  'AAGG', 'CTTTAGC' ), # rb/4/7
            8:  ( 'CCCGA', 'TCTTCGC' ), # rb/5/7
            13: (  'ATCG', 'CGGCTT'  ), # rb/4/6
            26: (  'TAGG', 'CTGCTCGC'), # rb/4/8, ends with TCGC like rbf(8)
            39: ( 'ACCTG', 'CTGTAGA' ), # rb/5/7
            40: ( 'CCGAG', 'CCAGTCT' ), # rb/5/7
            47: (  'CCCG', 'CGAGAGCT'), # rb/4/8
            50: ( 'CGCGG', 'CCTAGG'  ), # rb/5/6
            51: ( 'GCTGA', 'TCGGGCT' ), # rb/5/7
            53: (  'CGTG', 'CTTATGC' ), # rb/4/7
            56: (  'TCGC', 'GCCTGC'  ), # rb/4/6
            68: (  'CCAG', 'CTGCCAGC'), # rb/4/8
            74: (  'ATCG', 'CGCTGCTT'), # rb/4/8
            99: (  'GCGG', 'CCGGGCTT'), # rb/4/8
           109: (  'ACGG', 'CCGGGCAT'), # rb/4/8
           134: (  'ATAG', 'CAGCAGC' ), # rb/4/7
           161: ('TGTGAG', 'CTCGGC'  ), # rb/6/6
    }
    aliases = {
        19: 8,
    }
    if i in aliases:
        raise ValueError("rbf({}) is the same as rbf({})".format(i, aliases[i]))
    if i not in linkers:
        raise ValueError("no sequence for rbf({})".format(i))

    sequenced_insert = aptamer(ligand)
    sequenced_insert.prepend(Domain("linker/5'", linkers[i][0]))
    sequenced_insert.append(Domain("linker/3'", linkers[i][1]))

    sgrna = wt_sgrna(target)
    sgrna.attach(
            sequenced_insert,
            'stem', 6,
            'stem', 24,
    )
    return sgrna

@design('rbb')
def randomize_bulge_backward(i, target='none', ligand='theo'):
    """
    rbb(4):
      Linkers are complementary to each other, but are predicted to be fully 
      base paired with or without theo.
    
    rbb(15):
      Linkers are complementary to each other, but are predicted to be fully 
      base paired with or without theo.
      
    rbb(27):
      Predicted to work.  The 5' linker sequence has some complementarity 
      with the aptamer.  When it base pairs with the aptamer, it forms a 
      bulge that apparently allows the aptamer to function.  When 
      theophylline is present, the 5' linker instead base pairs with the 3' 
      linker to form a stem that prevents Cas9 binding.  I think this linker- 
      linker interaction is a little weaker, because it has a CU mismatch in 
      the middle of an otherwise complementary region.

    rbb(29):
      Linkers are complementary to each other, but are predicted to be fully 
      base paired with or without theo.
      
    rbb(39):
      Linkers are complementary to each other, but are predicted to be fully 
      base paired with or without theo.
      
    rbb(42):
      Predicted to work.  The two linkers are perfectly complementary with the 
      exception of a UU mismatch.  In the apo-state, this is enough to allow a 
      bulge-like fold to form.  In the holo state, the bulge is gone.  I wonder 
      if this could be a generic design.  Despite being so close to the spacer, 
      the aptamer is insulated by the always-base-paired lower stem.  And the 
      change in base pairing is small, which means there shouldn't be a large 
      kinetic barrier.
      
    rbb(45):
      Linkers are complementary to each other, but are predicted to be fully 
      base paired with or without theo.
      
    """
    linkers = {
            # First screen
            4:  ('AAGCTG', 'CGGCGC'),   # rb/6/6
            15: ( 'CCCTA', 'TGGGGT'),   # rb/5/6
            27: ('GCGCTG', 'CGTCGC'),   # rb/6/6

            # Second screen
            29: ('GTCTGT', 'ATAGAT'),   # rb/6/6
            39: ('ACCTGC', 'GTAGGT'),   # rb/6/6
            42: ( 'ACCTC', 'GTGGT' ),   # rb/5/5
            45: ( 'CCCCC', 'GGGGGT'),   # rb/5/6

    }
    aliases = {
            19: 27,
            25: 27,
            41: 27,
            46: 45,
            47: 27,
            52: 27,
            53: 27,
            54: 45,
            69: 27,
            74: 27,
            77: 42,
            85: 39,
            89: 27,
            91: 29,
    }
    if i in aliases:
        raise ValueError("rbb({}) is the same as rbb({})".format(i, aliases[i]))
    if i not in linkers:
        raise ValueError("no sequence for rbb({})".format(i))

    sequenced_insert = aptamer(ligand)
    sequenced_insert.prepend(Domain("linker/5'", linkers[i][0]))
    sequenced_insert.append(Domain("linker/3'", linkers[i][1]))

    sgrna = wt_sgrna(target)
    sgrna.attach(
            sequenced_insert,
            'stem', 6,
            'stem', 24,
    )
    return sgrna

@design('rx')
def randomize_nexus(N, M, A=1, target='none', ligand='theo'):
    """
    Flank the aptamer with a random sequence on either side and insert it into 
    the nexus.

    The insertion replaces the wildtype sequence from the 'GG' of the critical 
    2bp stem to the 'CC' of that same stem.  This stem is fairly sensitive to 
    mutation, but it isn't totally immutable.  Not all base-paired sequences 
    are functional (e.g. 'GG...CC' works but 'CC...GG' doesn't) but I estimate 
    from the data in the Briner paper that about half are, at least to some 
    extent.  There are 256 4bp sequences, of which 16 are perfectly based 
    paired.  If half of those 16 are actually functional, then I expect only 
    8/256 = 3% of the sequences in this library to be functional.

    I'm not too worried about this library having a lot of nonfunctional 
    members, for two reasons.  First, I don't anticipate this being a very big 
    library.  This library only needs to recapitulate a 2bp stem, while the 
    bulge and hairpin libraries need to recapitulate a 4bp stem.  It'll be 
    easier to fully cover a small library, so I don't need to worry about 
    nonfunctional members diluting functional ones.  Second, the first step in 
    the screen is for functional members, so I should get rid of the chaff 
    quickly.

    Parameters
    ----------
    N: int
        The number of random nucleotides to put 5' of the aptamer.  I 
        anticipate N being between 2 and 5, enough to recapitulate the stem and 
        to add some possible interactions above it.
        
    M: int
        The number of random nucleotides to put 3' of the aptamer.  I 
        anticipate N being between 2 and 5, enough to recapitulate the stem and 
        to add some possible interactions above it.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            random_insert(ligand, N, M),
            'nexus', 2,
            'nexus', 11,
    )
    return sgrna

@design('rxb')
def randomize_nexus_backwards(i, dang_sgrna=False, keep_stem=0, target='none', ligand='theo', species='sp', pam=None):
    """
    Most of these designs are not predicted to fold correctly in either 
    condition.  The exception is rxb(51), for which the lower stem is predicted 
    to fold better without ligand than with it.
    """
    linkers = {
            2:  ('GGGGA', 'TCTCC'),     # rx/5/5
            11: ('GTGGG', 'CCTAC'),     # rx/5/5
            14: ('GAAGG', 'CTTTC'),     # rx/5/5
            22: ('GGTG',  'CATCT'),     # rx/4/5
            39: ('GGGGA', 'TCTTC'),     # rx/5/5
            44: ('GGGGA', 'TTTGC'),     # rx/5/5
            51: ('GCCCG', 'CGAGT'),     # rx/5/5
            91: ('GGGAA', 'TTCC'),      # rx/5/4
            94: ('GTG',   'CAC'),       # rx/3/3

            # Manually swap the GU base pair in the middle of rxb/11.  My 
            # hypothesis is that Cas9 needs to interact with that U, and that 
            # the aptamer controls whether it's flipped out and available to 
            # Cas9 or sequestered in a base pair.  Swapping the GU base pair 
            # tests this hypothesis by changing the position of the U without 
            # changing the strength of the stem.
            '11a': ('cTGGG', 'CCTAg'),
            '11b': ('GaGGG', 'CCTtC'),
            '11c': ('GTtGG', 'CCgAC'),
            '11d': ('GTGcG', 'CgTAC'),
            '11e': ('GTGGc', 'gCTAC'),
    }
    aliases = {
            19: 14,
            26: 14,
            41: 2,
            52: 11,
            54: 11,
            61: 11,
            66: 14,
            68: 2,
            70: 2,
            88: 11,
            93: 51,
            '11u': '11c'
    }
    if i in aliases:
        raise ValueError("rxb({}) is the same as rxb({})".format(i, aliases[i]))
    if i not in linkers:
        raise ValueError("no sequence for rxb({})".format(i))

    linker_5 = Domain('linker/5', linkers[i][0])
    linker_5.style = 'red'
    linker_3 = Domain('linker/3', linkers[i][1])
    linker_3.style = 'red'

    sequenced_insert = aptamer(ligand)
    sequenced_insert.prepend(linker_5)
    sequenced_insert.append(linker_3)

    if dang_sgrna:
        sgrna = on(pam=pam, target=target, species=species)

        Lx = len(sgrna['nexus/3'])
        if keep_stem > Lx:
            raise ValueError("nexus stem is {} bp, can't keep {}".format(Lx, keep_stem))

        sgrna.attach(
                sequenced_insert,
                'nexus/5', 0  + keep_stem,
                'nexus/3', Lx - keep_stem,
        )
    else:
        sgrna = wt_sgrna(target)
        sgrna.attach(
                sequenced_insert,
                'nexus', 2,
                'nexus', 11,
        )

    return sgrna

@design('rh')
def randomize_hairpin(N, M, dang_sgrna=False, target='none', ligand='theo'):
    """
    Flank the aptamer with a random sequence on either side and insert it into 
    the first hairpin.

    The insertion replaces the first hairpin and the 4 nucleotides 5' of it, 
    which are AUCA in the wildtype sgRNA.  Those 4 upstream residues are 
    interesting for a number of reasons.  First of all, the data from the 
    Briner paper show that sequence changes in this region have a moderate 
    effect on sgRNA function that lengthening this region can ameliorate the 
    effects of truncating the hairpin.  I think the ability of this upstream 
    region to have a moderate effect on sgRNA makes it a good candidate for 
    randomization.

    Beyond that, the wildtype sequence is "AUCA", which is an "ANYA" tetraloop.
    I don't think that this sequence actually folds into a tetraloop in the 
    wildtype sgRNA, but the sh() family of designs is supposed to use the 
    tetraloop to make base pairs between the nexus and the hairpin in the off 
    state.  Some of the sh() designs were functional, so allowing the tetraloop 
    to optimize seems like a promising direction.

    Parameters
    ----------
    N: int
        The number of random base pairs to put 5' of the aptamer.  I anticipate 
        N being between 6 and 8, where 8 is the wildtype length.
        
    M: int
        The number of random base pairs to put 3' of the aptamer.  I anticipate 
        N being between 4 and 6, where 4 is the wildtype length.
    """
    sgrna = wt_sgrna(target)
    sgrna.attach(
            random_insert(ligand, N, M),
            'hairpins', 1,
            'hairpins', 17,
    )
    return sgrna

@design('rhi')
def randomize_hairpin_i(N, M=None, target='none', ligand='theo'):
    """
    Flank the aptamer with a random sequence on either side and insert it into 
    the first hairpin.

    This is a variant of the rh library.  Unlike rh, this library focuses 
    exclusively on the stem connecting the sgRNA to the aptamer and does not 
    randomize the ruler at all.*  This is change in focus is based on two 
    things.  First, I want to screen the library in yeast.  Because yeast are 
    much less competent than bacteria, I need to make my libraries smaller to 
    compensate.  Second, the mutations in the ruler didn't play a part in the 
    ``rhf 6`` mechanism, as predicted by RNAfold.  RNAfold has been wrong 
    before, but in this case I think it's reasonable to prioritize the actual 
    communication module.

    * This library also exclusively uses the Dang scaffold.

    Parameters
    ----------
    N: int
        The number of random base pairs to put 5' of the aptamer.  I anticipate 
        N being between 4 and 6, where 4 is the wildtype length.
        
    M: int [optional]
        The number of random base pairs to put 3' of the aptamer.  I anticipate 
        M being between 4 and 6, where 4 is the wildtype length.  By default, M 
        will be the same as N.
    """
    if M is None: M = N
    sgrna = on(target=target)
    sgrna['hairpin/5'].attachment_sites = 0,
    sgrna['hairpin/3'].attachment_sites = 4,
    sgrna.attach(
            random_insert(ligand, N, M),
            'hairpin/5', 0,
            'hairpin/3', 4,
    )
    return sgrna

@design('rhf')
def randomize_hairpin_forward(i, expected_only=False, target='none', ligand='theo'):
    """
    rhf(6):
        The 3' link can base pair with the 'GUC' motif in the nexus, while the 
        5' link can base pair with the aptamer.  The 3' end of the nexus can 
        also base pair with the aptamer due to an unexpected point mutation 
        outside of either link.  Folding simulations predict that this design 
        will work with several different spacers: GFP, RFP, and none.  The 
        prediction for the AAVS spacer is ambiguous.  In reality, rhf(6) has 
        15x activity with the GFP spacer and 1.5x activity with the RFP spacer.
    """
    linkers = {
            6: ('TTCGCCG', 'CGAC'),     # rh/7/4
    }
    aliases = {
            14: 6,
            22: 6,
            31: 6,
            72: 6,
            73: 6,
    }
    if i in aliases:
        raise ValueError("rhf({}) is the same as rhf({})".format(i, aliases[i]))
    if i not in linkers:
        raise ValueError("no sequence for rhf({})".format(i))

    sequenced_insert = aptamer(ligand)
    sequenced_insert.prepend(Domain("linker/5'", linkers[i][0]))
    sequenced_insert.append(Domain("linker/3'", linkers[i][1]))

    sgrna = wt_sgrna(target)
    sgrna.attach(
            sequenced_insert,
            'hairpins', 1,
            'hairpins', 17,
    )

    if not expected_only and i == 6:
        sgrna['nexus'].mutate(11, 'C')

    return sgrna

@design('mx', 'dx')
def modify_nexus(N, target='none', ligand='theo'):
    """
    Randomize the region 3' of the evolved linker from rxb/11, the strongest 
    sensor from the rxb screen, keeping the linker itself unchanged.  The 
    purpose of this strategy is to create a library that is highly enriched 
    with functional sensors, so that we can be fairly stringent while we screen 
    for sensors that are not specific to any one targeting sequence.

    We chose to randomize the region 3' of the evolved linker to minimize the 
    chance that the mutations will interact with the targeting sequence (by 
    virtue of being relatively far away in the primary sequence).  The argument 
    N gives the number of nucleotides, counting 3' from the base of the evolved 
    stem, to mutate.  If any nucleotides that are part of the hairpin stem 
    would be randomized, their base-pairing partner is also randomized.

    Parameters
    ----------
    N: int
        The number of nucleotides, counting 3' from the base of the evolved 
        stem, to randomize.  Note that the actual number of randomized position 
        may be greater than N, because positions being randomized in the 
        hairpin stem will automatically include their base-pairing partner.

    I was considering both rxb/11 and rxb/2 as the template for this library.  
    I ultimately decided to use rxb/11 for two reasons.  First, it was slightly 
    more common than rxb/2, suggesting that it was at least slightly more fit.  
    Second, rxb/11 turned off almost all the way without ligand while rxb/2 
    turned on almost all the way with ligand.  Since backward designs should 
    effectively activate transcription, it's better than they turn all the way 
    off.
    """

    # Base this library on the optimized sgRNA described by Dang et al.
    sgrna = on(target=target)

    # Use the communication module from rxb/xxx.
    sgrna['nexus/5'].seq = 'GTGGG'
    sgrna['nexus/3'].seq = 'CCTAC'

    # Insert the aptamer into the nexus.
    sgrna['nexus/o'].attachment_sites = 0,5
    sgrna.attach(aptamer(ligand), 'nexus/o', 0, 'nexus/o', 5)

    # Randomize the specified number of nucleotides 3' of the nexus.
    if N < 0 or N > 11:
        raise ValueError("dh: N must be between 0 and 11, not {}".format(N))
    
    Lr = len(sgrna['ruler'])
    Nr = max(min(N, Lr), 0)
    Nh = max(min(N - Lr, 4), 0)

    sgrna['ruler'].seq = ('N' * Nr) + sgrna['ruler'][Nr:]
    sgrna['hairpin/5'].seq = ('N' * Nh) + sgrna['hairpin/5'][Nh:]
    sgrna['hairpin/3'].seq = sgrna['hairpin/3'][:4-Nh] + ('N' * Nh)

    return sgrna

@design('mh')
def modify_hairpin(N, A=1, target='none', ligand='theo', species='sp', pam=None):
    """
    Insert the aptamer into the hairpin and build a library by randomizing 
    the positions that were most likely to mutate in Monte Carlo RNA design 
    simulations.

    The score function in the Monte Carlo simulations was the probability that 
    the sgRNA would adopt the active fold with ligand and would not adopt it 
    without the ligand.  These probabilities were obtained by dividing the 
    partition function for the active macrostate by the partition function for 
    the entire ensemble.  The partition functions were calculated by ViennaRNA 
    and the active macrostate was defined and simulated using constraints.
    
    The sampling moves in the Monte Carlo simulations were simply point 
    mutations made randomly to selected positions.  Positions that were 
    constrained to be base paired were mutated such that the base pair was 
    maintained and the overall distribution of nucleotides was not biased.  GU 
    pairs were not sampled at these positions.

    500 rounds of simulated annealing were carried out, and more than 300 
    independent, high-scoring sequences were picked from those trajectories.  
    These sequences were visualized as a sequence logo.

    Based on the ``best_library_size.py`` script and the empirical observation 
    that in my rbf screens I found about as many N=10 sequences and N=12 ones, 
    I wanted to randomize 11 positions.  I chose to randomize the 5 position in 
    between the nexus stem and 4 or 5 positions in between the nexus and the 
    hairpin (a region I'm calling the "ruler").  Instead of randomizing the 
    hairpin stem linking the aptamer to the sgRNA, I used the linker sequence 
    from rhf(6).  It's a stem of length four with three GC pairs and one CA 
    mismatch.
    
    Parameters
    ----------
    N: int
        The length of the ruler domain, which must be either 6 or 7.  The 
        natural length of this domain is 7, but it is of length 6 in rhf(6).
    """

    # Base this library on the optimized sgRNA described by Dang et al.
    sgrna = on(pam=pam, target=target, species=species)

    # Randomize the top of the nexus.  This region is predicted to be important 
    # for allowing the sgRNA to work with multiple spacers.
    sgrna['nexus/o'].seq = 'NNNNN'

    # Randomize most of the nucleotides connecting the nexus to the hairpins.  
    # This region is also predicted to be important for allowing the sgRNA to 
    # work with multiple spacers.
    if N == 7:
        sgrna['ruler'].seq = 'NNNAUNN'
    elif N == 6:
        sgrna['ruler'].seq = 'NNAUNN'
    else:
        raise ValueError("mh: N must be either 6 or 7")

    # Insert the aptamer into the hairpin.
    apt = aptamer(ligand)
    sgrna['hairpin/o'].attachment_sites = 0,4
    sgrna.attach(apt, 'hairpin/o', 0, 'hairpin/o', 4)

    # Use the sequence found in rhf/6 to link 
    sgrna['hairpin/5'].seq = 'GCCG'
    sgrna['hairpin/3'].seq = 'CGAC'

    return sgrna

@design('mhf')
def modify_hairpin_forward(i, expected_only=False, target='none', ligand='theo', species='sp', pam=None):
    linkers = {
            3:  ('CGGTC', 'GTC', 'CA'),
            4:  ('ACGAA', 'GTA', 'CC'),
            7:  ('TCTGA', 'AG',  'CC'),
            13: ('TGACA', 'GC',  'CC'),
            16: ('TGGTA', 'AT',  'CC'),
            20: ('TAAAC', 'CTC', 'CA'),
            21: ('ATCCT', 'CGC', 'GC'),
            25: ('ACGTC', 'GC',  'TC'),
            26: ('TTCGT', 'GCC', 'TC'),
            30: ('GTGTC', 'GT',  'AC'),
            35: ('GCACT', 'TA',  'CC'),
            37: ('TCTTC', 'CGC', 'CC'),
            38: ('ACGGT', 'CGC', 'CC'),
            41: ('ACTCT', 'GT',  'CG'),
    }
    aliases = {
            29: 21,
    }
    unexpected_muts = {
            4:  ('upper_stem/5', 8, 'T'),
            7:  ('upper_stem/5', 3, 'T'),
            13: ('upper_stem/5', 3, 'T'),
            21: ('upper_stem/3', 3, 'A'),
            26: ('upper_stem/3', 3, 'T'),
            35: ('upper_stem/5', 5, 'A'),
            37: ('upper_stem/5', 2, ''),
            38: ('upper_stem/5', 2, 'C'),
    }

    if i in aliases:
        raise ValueError("mhf({}) is the same as mhf({})".format(i, aliases[i]))
    if i not in linkers:
        raise ValueError("no sequence for mhf({})".format(i))
    if expected_only and i not in unexpected_muts:
        raise ValueError("mhf({}) doesn't have any unexpected mutations.".format(i))

    N = len(''.join(linkers[i])) - 5 + 2
    sgrna = mh(N, ligand=ligand, target=target, pam=pam, species=species)
    sgrna['nexus/o'].seq = linkers[i][0]
    sgrna['ruler'].seq = linkers[i][1] + 'AU' + linkers[i][2]

    if not expected_only and i in unexpected_muts:
        domain, idx, nuc = unexpected_muts[i]
        sgrna[domain].mutate(idx, nuc)

    return sgrna

@design('qh')
def seqlogo_hairpin(N, target='none', ligand='theo', pam=None):
    """
    Randomize the stem linking the aptamer to the sgRNA and the parts of the 
    sgRNA that were the most conserved after being randomized in previous 
    screens.  Specifically, I identified these conserved positions by looking 
    at a sequence logo of the relatively few (≈20) clones I sequenced from my 
    previous screen.  The theory behind this strategy is that positions with 
    a clear preference for some nucleotides over others are more likely to be 
    important for sensor activity.

    In this case, the previous screen was ``mhf`` and the sequence logo showed 
    that all three positions in the ruler that were randomized had a preference 
    for a non-native nucleotide.  (In fact, the preference was for C in all 
    three cases.)  The ``mhf`` screen kept two positions in the ruler fixed, 
    but since these positions were flanked by important-seeming positions on 
    both sides, I decided to randomize the whole ruler this time.

    I am also randomizing the stem (often called a communication module) that 
    connects the aptamer to the sgRNA.  The ``N`` parameter dictates how long 
    this stem should be, in base pairs, not counting any base pairs that are 
    implicitly included with the aptamer.  (Note: I realized that including one 
    base pair on the end of the aptamer domain makes simulating the whole 
    construct easier, so all the new aptamers include one base pair like that.  
    But the theophylline aptamer predates this realization, so it doesn't.)

    Parameters
    ----------
    N: int
        The length of the communication module, in base pairs.  Recommended 
        values are 3 and 4.
    """

    # Make sure the length of the communication module makes sense.
    if N < 0:
        raise ValueError('qh: N must be >= 0')

    # Base this library on the optimized sgRNA described by Dang et al.
    sgrna = on(pam=pam, target=target)

    # Randomize the entire ruler.
    sgrna['ruler'].seq = 'GU' + 'N' * (len(sgrna['ruler']) - 2)

    # Randomize the communication module.
    sgrna['hairpin/5'].seq = N * 'N'
    sgrna['hairpin/3'].seq = N * 'N'

    # Insert the aptamer above the communication module.
    sgrna['hairpin/o'].attachment_sites = 0,4
    sgrna.attach(aptamer(ligand), 'hairpin/o', 0, 'hairpin/o', 4)

    return sgrna

@design('ph')
def protein_binding_hairpin(N, target='none', ligand='theo', pam=None):
    """
    Randomize the region 5' of the hairpin in the hopes of creating a sequence 
    that is partially complementary to the aptamer.  Presently, this strategy 
    is intended for protein binding aptamers like MS2 that aren't expected to 
    have significantly different bound and unbound conformations.  The hope is 
    that protein binding can stabilize an otherwise minor conformation (i.e. 
    conformational selection) and lock the sgRNA into an active or inactive 
    state.

    This strategy is unbalanced because rather than randomizing stretches of 
    nucleotides on both sides of the aptamer and hoping for a stem that will 
    respond to the ligand, we are only randomizing nucleotides on one side of 
    the aptamer and hoping that those nucleotides will interfere with the stem 
    formed naturally by the aptamer in a way that is sensitive to ligand.

    Parameter
    ---------
    N: int
        The number of nucleotides 5' of the hairpin to randomize.  The maximum 
        number is 12.  This is enough to extend almost throughout the nexus, 
        but the 2 bp stem in the nexus is always excluded.  The hairpin stem 
        itself is eliminated and totally replaced by the aptamer.
    """
    sgrna = on(pam=pam, target=target)

    # Replace the hairpin with the aptamer.
    sgrna['hairpin/5'].attachment_sites = 0,
    sgrna['hairpin/3'].attachment_sites = 4,
    sgrna.attach(aptamer(ligand), 'hairpin/5', 0, 'hairpin/3', 4)

    # Randomize the specified number of nucleotides 5' of the hairpin.
    Lr  = len(sgrna['ruler'])
    Lx = len(sgrna['nexus/o'])
    L = Lr + Lx

    if N < 0 or N > L:
        raise ValueError("rh: N must be between 0 and {}, not {}".format(L, N))

    Nr = clamp(N,      0, Lr)
    Nx = clamp(N - Lr, 0, Lx)

    sgrna['ruler'].seq = sgrna['ruler'][:Lr-Nr] + ('N' * Nr)
    sgrna['nexus/o'].seq = sgrna['nexus/o'][:Lx-Nx] + ('N' * Nx)

    return sgrna

@design('ux')
def sequester_u59_nexus(N, M, keep_bottom_gc=False, target='none', ligand='theo', pam=None):
    """
    James says:

    I'm going to try the uracil sequestering strategy and randomize positions I
    think are important from my inspection of the crystal structure 4UN3. The
    thiamine aptamer will replace the nexus/o sequence.

    I ultimately decided to insert the thiamine aptamer into the nexus hairpin and randomize positions in the nexus
    stem region. The uracil that flips out in the functional sgRNA remains as WT. I added a variable number of random
    nucleotides between the end of the stem region and the beginning of the aptamer to serve as a connector. Hopefully
    this will also promote base pairing with other parts of the sgRNA to form alternative stable non-funcitonal
    conformations that can be escaped through binding of TPP.

    :param target:
    :param ligand:
    :return:
    """
    sgrna = on(pam=pam, target=target)

    # Work out what to do with the bottom-most base pair.  This base pair can't 
    # be strand-swapped, so it seems important in a way I don't understand.  
    # For this reason, the library provides an option to keep it as is.
    if keep_bottom_gc == 'g':
        bottom_5 = 'G'
        bottom_3 = 'C'
        n = N + 1
        m = M - 1
    else:
        bottom_5 = ''
        bottom_3 = 'N'
        n = N
        m = M - 2

    # Check arguments.
    if n < 2: raise ValueError("N must be ≥ 2 (or ≥ 1 if the bottom base pair is being kept)")
    if m < 0: raise ValueError("M must be ≥ 2 (or ≥ 1 if the bottom base pair is being kept)")

    # Randomize the nexus base pairing
    sgrna['nexus/5'].seq = bottom_5 + ('N' * N)
    sgrna['nexus/5'].style = 'white', 'bold'
    sgrna['nexus/3'].seq = ('N' * m) + 'UN' + bottom_3
    sgrna['nexus/3'].style = 'white', 'bold'

    # Insert the aptamer in the nexus hairpin loop
    sgrna['nexus/o'].style = 'white', 'bold'
    sgrna['nexus/o'].attachment_sites = 0,5
    sgrna.attach(aptamer(ligand), 'nexus/o', 0, 'nexus/o', 5)

    return sgrna

@design('uh')
def sequester_u59_hairpin(N, M, target='none', ligand='theo', pam=None):
    """
    Parameters
    ==========
    N: int
        Length of the loop in the nexus.  This region is intended to base pair 
        with the aptamer in a way that sequesters U59.  Typical this argument 
        would be between 4 and 6.

    M: int
        Length of the ruler. Typically either 6 or 7.
    """

    # When designing this library, I had to choose between randomizing:
    # - the AA on the very 5' side of the nexus.
    # - the length of the nexus loop.
    # - the hairpin stem (in part or in full).
    #
    # I didn't want to randomize more than 12 residues, and I already had 10 
    # residues that I definitely wanted to randomize, so I could only choose 
    # one of these regions to randomize.
    #
    # I decided against randomizing the AA on the 5' side of the nexus because 
    # I felt it would be better to just add random nucleotides to the loop.  
    # The point of randomizing those nucleotides would've been to allow the 
    # nexus to base pair with the aptamer.  But adding random nucleotides to 
    # the nexus rather than randomizing the AA gives the library a bigger 
    # contiguous stretch of nucleotides to work with, and I think that's more 
    # likely to have something good.
    #
    # I decided against randomizing the hairpin stem for more pragmatic 
    # reasons.  Because the hairpin spans the aptamer and most of my 
    # alternative aptamers are quite long, constructing a library that 
    # randomizes most of the nexus, adds a large aptamer, and randomizes part 
    # of the hairpin stem would require very long primers.  If only the nexus 
    # is being randomized, I can assemble the library in two steps using short 
    # primers for both assemblies.  I could get around this problem by only 
    # randomizing one side of the stem, but I think this would too severely 
    # limit the ability of that region to form base pairs.
    #
    # So in the end I decided to randomize the length of the nexus loop.  This 
    # gives the most contiguous variation, which I think will be helpful for 
    # forming the base-pairs needed to make a sensor.

    # Base this library on the optimized sgRNA described by Dang et al.
    sgrna = on(pam=pam, target=target)

    # Randomize the nexus.
    sgrna['nexus/o'].seq = N * 'N' + 'U'

    # Randomize the ruler.  I think it's important to randomize this region 
    # because there are two roles I can imagine it fulfilling.  First, it could 
    # form base-pairing interactions that would help sequester U59.  Second, it 
    # could be the loop in a stem between the nexus and the aptamer.
    #
    # I also reduce the length of the ruler by one nucleotide relative to the 
    # positive control.  This mimics mhf/30 and reduces the complexity of the 
    # library.
    sgrna['ruler'].seq = M * 'N'

    # I have two options with regard to the first hairpin stem:
    # - Randomize it (in part or in full).
    # - Use the sequence from rhf/6.
    #
    # Which option is best depends on how this stem contributes to the sensor.  
    # If it's participating in off-state base-pairs with the aptamer, then I'd 
    # want to randomize it to give it a chance to adapt to new aptamers.  If 
    # it's just allowing conformational changes in the aptamer to propagate to 
    # the rest of the sgRNA, then I'd want to use the sequence from rhf/6.
    #
    # I chose to use the sequence from rhf/6 because it simplifies the library 
    # construction (see above), I'm already randomizing 12 other positions, and 
    # this stem doesn't seem to be interacting with the aptamer in mhf/30.
    sgrna['hairpin/5'].seq = 'GCCG'
    sgrna['hairpin/3'].seq = 'CGAC'

    # Insert the aptamer above the communication module.
    sgrna['hairpin/o'].attachment_sites = 0,4
    sgrna.attach(aptamer(ligand), 'hairpin/o', 0, 'hairpin/o', 4)

    return sgrna

@design('uhf')
def sequester_u59_hairpin_forward(i, expected_only=False, target='none', ligand='theo', pam=None):
    """
    uhf 37:
        No predicted response to ligand.

    uhf 49:
        No predicted response to ligand.

    uhf 84:
        This design has strongly predicted differences in 2° structure between 
        apo and holo, although it's a little hard to rationalize why the holo 
        form is functional.  The nexus is predicted to form, except the 5' side 
        pairs with the ruler instead of the 3' side.  The stem is 5 bp long and 
        has two GU pairs in the middle, one of which probably has to be flipped 
        out.  In the apo fold, the nexus basically pairs with the terminator.

    uhf 135:
    """
    linkers = {
            8:   ('CGCAG',  'GTCCCT'),  # First try
            30:  ('CCTG',   'GTGATCA'),
            37:  ('GCAGG',  'GTTCCCA'),
            49:  ('CTAGG',  'GTTCCCG'),
            66:  ('CAGAGG', 'GTTCCT'),
            71:  ('TTCAC',  'GTTCCCA'),
            84:  ('GCGAG',  'GTTCCCA'),
            132: ('CGCCAG', 'GTTCCT'),  # Second try
            135: ('TTTGA',  'GTTCAGG'),
            160: ('CCCTG',  'GCGATCA'),
            174: ('CTTG',   'GCGCTG'),
    }
    aliases = {
            57: 8,
            62: 37,
            89: 84,
            137: 132,
            170: 132,
            172: 132,
            173: 160,
            179: 160,
            182: 132,
    }
    unexpected_muts = {
            8:   ('upper_stem/o', 0, 'T'),
            66:  ('upper_stem/5', 3, 'T'),
            132: ('upper_stem/5', 8, 'T'),
            135: ('upper_stem/5', 3, ''),
            160: ('upper_stem/o', 0, 'T'),
            174: ('upper_stem/5', 8, 'T'),
    }

    if i in aliases:
        raise ValueError("uhf({}) is the same as uhf({})".format(i, aliases[i]))
    if i not in linkers:
        raise ValueError("no sequence for uhf({})".format(i))
    if expected_only and i not in unexpected_muts:
        raise ValueError("uhf({}) doesn't have any unexpected mutations.".format(i))

    sgrna = uh(0, 0, ligand=ligand, target=target, pam=pam)
    sgrna['nexus/o'].seq  = linkers[i][0] + 'U'
    sgrna['nexus/o'].style = 'white'
    sgrna['ruler'].seq    = linkers[i][1]
    sgrna['ruler'].style = 'white'

    if not expected_only and i in unexpected_muts:
        domain, idx, nuc = unexpected_muts[i]
        sgrna[domain].mutate(idx, nuc)

    return sgrna

@design('m11')
def modulate_rxb_11_1(seq='', target='none', ligand='theo', species='sp'):
    """
    Attempt to modulate the leakiness of rxb 11,1 by changing the strength of 
    the base-pairs above U94.

    This design strategy is based off the hypothesis that rxb 11,1 works by 
    controlling the ability of U94 (which corresponds to U59 in wt sgRNA) to 
    flip out and interact with Cas9.  In turn, this hypothesis is based on the 
    claim made by Kyle Watters (citing unpublished data) that wildtype sgRNA 
    can only bind Cas9 if U59 is unpaired.

    In rxb 11,1, U94 forms a wobble base pair in the middle of a 5 bp stem:

        [aptamer]
           G=C
           G=C
           G·U ←94
           U-A
        5' G=C 3'

    The hypothesis is that when no ligand is present, the base of the aptamer 
    comes apart and allows the top of the stem to melt, which allows U94 to 
    flip out and interact with Cas9.  When ligand is present, the base of the 
    aptamer comes together, locks the stem in place, and prevents U94 from 
    flipping out.

    If this hypothesis is correct, we should be able to modulate how well rxb 
    11,1 turns on or off by increasing or decreasing, respectively, the 
    strength of the base pairs above it.  For example, replacing one or both of 
    the GC base pairs with AU base pairs should allow the top of the stem to 
    melt more easily, which should create a sensor that turns on better.  
    Likewise, increasing the length of the stem should make it harder for U59 
    to flip out, which should create a sensor that turns off better.

    Parameters
    ==========
    seq: str
        The sequence to install on the 5' side of the nexus above U94.  The 
        usual base pairs can be specified with "a", "c", "g", and "u".  Wobble 
        base pairs can be specified with "h" (GU pair) and "v" (UG pair).  The 
        sequence is case-insensitive.  The value corresponding to the original 
        rxb 11,1 sequence is "gg".
    """
    sgrna = rxb(11, 1, target=target, ligand=ligand, species=species)

    seq_5, seq_3 = base_pair(seq)
    sgrna['linker/5'].replace(3, 5, seq_5)
    sgrna['linker/3'].replace(0, 2, seq_3)

    return sgrna

@design('won')
def strand_swap_on(nuc=None, target='none'):
    """
    Strand-swap the first position in the nexus stem.
    """
    sgrna = on(target=target)

    nexus_5 = sgrna['nexus/5'].seq
    nexus_3 = sgrna['nexus/3'].seq

    if nuc is not None:
        swap_5, swap_3 = base_pair(nuc)
    else:
        swap_5, swap_3 = nexus_3[-1], nexus_5[0]

    sgrna['nexus/5'].mutate(0, swap_5)
    sgrna['nexus/3'].mutate(1, swap_3)

    return sgrna

@design('w11')
def strand_swap_rxb_11_1(N, nuc=None, target='none', ligand='theo', species='sp'):
    """
    Make strand-swapping mutations to test my proposed mechanism for rxb 11,1.

    The hypothesis I want to test is that rxb 11,1 works by controlling the 
    ability of U94 (which corresponds to U59 in wt sgRNA) to flip out and 
    interact with Cas9.  This hypothesis is based on the claim made by Kyle 
    Watters (citing unpublished data) that wildtype sgRNA can only bind Cas9 if 
    U59 is unpaired.  
    
    In rxb 11,1, U94 forms a wobble base pair in the middle of a 5 bp stem:

        [aptamer]
           G=C
           G=C
       64→ G·U ←94
           U-A
        5' G=C 3'

    The hypothesis is that when no ligand is present, the base of the aptamer 
    comes apart and allows the top of the stem to melt, which allows U94 to 
    flip out and interact with Cas9.  When ligand is present, the base of the 
    aptamer comes together, locks the stem in place, and prevents U94 from 
    flipping out.

    If this hypothesis is correct, swapping G64 and U94 should have a severe 
    detrimental effect on the sensor, because U94 will no longer be in a 
    position to interact with Cas9 (despite the fact that this mutation does 
    not change the strength of the nexus stem).  But swapping any of the other 
    base pairs in the nexus stem should have no effect.

    Parameters
    ==========
    N: int
        The position in the nexus stem to swap.  Positions 1 and 5 correspond 
        to the base pairs furthest and closest to the aptamer, respectively.
    """
    if N < 1 or N > 5:
        raise ValueError('N must be between 1 and 5, not {}'.format(N))

    sgrna = rxb(11, 1, target=target, ligand=ligand, species=species)

    linker_5 = sgrna['linker/5'].seq
    linker_3 = sgrna['linker/3'].seq

    if nuc is not None:
        swap_5, swap_3 = base_pair(nuc)
    else:
        swap_5, swap_3 = linker_3[5-N], linker_5[N-1]

    sgrna['linker/5'].mutate(N-1, swap_5)
    sgrna['linker/3'].mutate(5-N, swap_3)

    return sgrna

@design('w30')
def strand_swap_mhf_30(N, model=None, target='none', ligand='theo'):
    """
    Make strand-swapping mutations to probe the mechanism of mhf/30.

    Our goal with these mutations is to determine the structure of mhf/30 in 
    its apo (inactive) and holo (active) states.  For the active (holo) state, 
    the hypothesis is clear: the ends of the aptamer come together to form the 
    hairpin stem, and the GGG/CCC stem plays the role of the nexus.  For the 
    inactive (apo) state, we have two models.  In one, the aptamer is mostly 
    pre-ordered and the 5' half of the hairpin stem is sequestering the 
    pseudo-nexus.  In the other, the aptamer is not pre-ordered and is instead 
    base-pairing with the pseudo-nexus itself.

    Because we believe that the apo and holo states are very different, and we 
    are very unsure about the structure of the apo state, it's hard to design 
    mutants that will have predictable effects.  The approach we're taking here 
    is to strand-swap all the base-pairs in the active state (which we are 
    fairly confident in) and to see how that affects the inactive state.  Most 
    often (but not always), the predicted effect will be to weaken the inactive  
    state.  It these cases, the two models often predict that the inactive 
    state can be rescued by different compensatory mutations or strand-swaps, 
    so we will test those too.

    Parameters
    ==========
    N: int
        The position to swap.  The allowed positions are: 63-65, 77-80.

    model: int
        If given, make a compensatory mutation according to the given model.  
        Not all mutations have compensatory mutations.
    """

    if not (63 <= N <= 65) and not (77 <= N <= 80):
        raise ValueError('N must be between 63-65 or 77-80, not {}'.format(N))

    sgrna = mhf(30, target=target, ligand=ligand)

    def swap(i):
        j = swaps[i]

        i_nuc = get(i)
        j_nuc = get(j)

        mutate(i, j_nuc)
        mutate(j, i_nuc)

    def mutate(i, nuc):
        domain, rel_i = key(i)
        sgrna[domain.name][rel_i] = nuc.lower()

    def get(i):
        domain, rel_i = key(i)
        return sgrna[domain.name][rel_i]

    def key(i):
        # We can't just use position i at face value, because we don't know if 
        # there's a spacer or not.  So we'll first subtract 21 (20 for the 
        # spacer, 1 for the 1-indexing) from the index and then add back the 
        # index of the first position in the upper stem (20 if there is a 
        # spacer, 0 if not).
        i = i - 21 + sgrna.index_from_domain('lower_stem/5', 0)
        return sgrna.domain_from_index(i)


    swaps = {
            63: 71,
            64: 70,
            65: 69,
            77: 111,
            78: 110,
            79: 109,
            80: 108,
    }
    models = {
            1: {
                63: None,
                64: lambda: swap(80),
                65: lambda: mutate(79, 'G'),
                77: lambda: mutate(67, 'C'),
                78: lambda: mutate(66, 'G'),
                79: lambda: mutate(79, 'C'),
                80: lambda: swap(64),
            },
            2: {
                63: lambda: swap(78),
                64: None,
                65: None,
                77: lambda: mutate(72, 'C'),
                78: lambda: swap(63),
                79: None,
                80: None,
            }
    }

    # Make the requested strand-swap.
    swap(N)

    # And make a mutation to test a particular model, if requested.
    if model is not None:
        if not models[model].get(N):
            raise ValueError('Model {} does not have a compensatory mutation for swapping position {}'.format(model, N))
        models[model][N]()

    return sgrna

@design('m30')
def mutate_mhf_30(mut, target='none', ligand='theo'):
    """
    Test the hypothesis that mhf/30 works by switching between an inactive 
    conformation in which C80 and G64 are base-paired, and an active 
    conformation in which C80 and G108 are base-paired.

    Parameter
    ---------
    mut: str
        A string of length 3 where the first character indicates the nucleotide 
        to install at position 64, the second indicates position 80, and the 
        third indicates position 108.
    """
    sgrna = mhf(30, target=target, ligand=ligand)

    sgrna['nexus/5'][1] = mut[0].upper()
    sgrna['hairpin/5'][2] = mut[1].upper()
    sgrna['hairpin/3'][1] = mut[2].upper()

    return sgrna

@design('bu')
def MS2_forwards_upperstem(N, M, target='none', ligand='theo', pam=None):
    """
    James says:

    Referencing the crystal structure of the aptamer-MS2 complex (PDB 1ZDI)

    Another useful paper:

    HORN, WILF T. et al. “The Crystal Structure of a High Affinity RNA Stem-
    Loop Complexed with the Bacteriophage MS2 Capsid: Further Challenges in
    the Modeling of ligand–RNA Interactions.” RNA 10.11 (2004)

    Observations from the crystal structure (PDB 1ZDI):

    The aptamer binds the surface created by the dimerization of two MS2
    subunits (better seen in PDB 2C50) where aptamer forms a mitt (looking at
    the back of my hand, 5' would be my thumb and 3' my pinkie). Since we do
    not expect a conformational change upon binding of MS2 to the aptamer, I
    want to think of ways that binding will either 1) sterically hinder sgRNA
    from being bound by Cas9 (backwards designs) or 2) induce refolding of the
    sgRNA from a non-functional state into a functional fold state (forward
    design).

    Here I outline my strategy for designing a library to generate a forward
    design sgRNA (hairpin/stem substitution). This borrows from your ph design (or
    at least what I remember from talking to you and looking at it before, I
    don't want to look at it now that I'm trying to design my own design
    strategy :P)

    The two locations in the sgRNA where we could feasibly insert the MS2
    aptamer without causing any obvious clashing is the upper stem and
    hairpin region. Considering the orientation of the aptamer after it is
    inserted into either of these sites, the upper stem region seems to be
    more feasible. The hairpin, and as the aptamer would after insertion, folds
    in towards Cas9, meaning that MS2 would be pressed right up against Cas9 if
    it is even able to bind at all. Where the same is true for the upper stem
    to an extent, it is more solvent accessible and an additional linker
    sequence would allow for more

    To get an idea of where to start, I am going to insert the MS2 aptamer in
    appropriate regions in the sgRNA and increment the number of base pairs to act
    as a spacer between the aptamer and the rest of the sgRNA.

    Trying: nexus, hairpin, upper stem

    :param target:
    :param ligand:
    :param pam:
    :return:
    """

    sgrna = on(pam=pam, target=target)

    assert N <= len(sgrna['upper_stem/5'].seq)
    assert M <= len(sgrna['upper_stem/3'].seq)

    sgrna['upper_stem/o'].attachment_sites = 0, 4
    sgrna.attach(aptamer(ligand), 'upper_stem/o', 0, 'upper_stem/o', 4)
    sgrna['upper_stem/5'].seq = 'GCUAUGCUG'[:N]
    sgrna['upper_stem/3'].seq = 'CAGCAUAGC'[9-M:]

    return sgrna

@design('bx')
def MS2_forwards_nexus(N, M, target='none', ligand='theo', pam=None):

    sgrna = on(pam=pam, target=target)

    assert N <= len(sgrna['nexus/5'].seq)
    assert M <= len(sgrna['nexus/3'].seq)

    sgrna['nexus/o'].attachment_sites = 0, 4
    sgrna.attach(aptamer(ligand), 'nexus/o', 0, 'nexus/o', 4)
    sgrna['nexus/5'].seq = 'GG'[:N]
    sgrna['nexus/3'].seq = 'CC'[2-M:]

    return sgrna

@design('bh')
def MS2_forwards_hairpin(N, M, target='none', ligand='theo', pam=None):

    sgrna = on(pam=pam, target=target)

    assert N <= len(sgrna['hairpin/5'].seq)
    assert M <= len(sgrna['hairpin/3'].seq)

    sgrna['hairpin/o'].attachment_sites = 0, 4
    sgrna.attach(aptamer(ligand), 'hairpin/o', 0, 'hairpin/o', 4)
    sgrna['hairpin/5'].seq = 'ACUU'[:N]
    sgrna['hairpin/3'].seq = 'AAGU'[4-M:]

    return sgrna

@design('ox')
def MS2_backwards_nexus(N, M, target='none', ligand='theo', pam=None):
    """
    Reference designs.MS2_forwards() for my library design rationale.

    Here I outline my strategy for designing a library to generate a backwards
    design sgRNA (nexus occlusion).

    My idea is that binding of MS2 to the aptamer/sgRNA complex will sterically
    occlude Cas9 from binding in a productive manner.

    Insertion of the aptamer into the nexus would place the bound MS2 in a
    clash with the basic alpha helix that runs through the folded sgRNA.

    :param target:
    :param ligand:
    :param pam:
    :return:
    """

    sgrna = on(pam=pam, target=target)

    # Literally the same strategy as ux...
