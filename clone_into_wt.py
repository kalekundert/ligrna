#!/usr/bin/env python3

"""\
Pick inverse PCR primers that can be used to clone a rationally designed sgRNA 
into a plasmid already harboring the wildtype sgRNA.

Usage:
    clone_into_wt.py <designs>... [options]

Options:
    -s, --spacer <name>     [default: gfp]
        The spacer sequence of the wildtype plasmid.  For some designs, this 
        doesn't matter because the primers won't overlap the spacer.  But for 
        other designs, particularly upper stem designs, different primers are 
        needed for each spacer.

    -c, --cut <index>
        Manually specify where the index where the insert should be split, 
        relative to the insert itself.  By default, the cut site is chosen to 
        make the primers the same length.  

    -t, --tm <celsius>      [default: 60]
        The desired melting temperature for the primers.

    -v, --verbose
        Show extra debugging output.
        
"""

def design_cloning_primers(name, spacer, cut=None, tm=60, verbose=False):
    import sgrna_sensor, itertools

    wt = sgrna_sensor.from_name('wt', target=spacer)
    design = sgrna_sensor.from_name(name, target=spacer)

    # Find where the design differs from the wildtype sgRNA:

    mismatch_5 = None
    mismatch_3 = None

    for i in itertools.count():
        if wt.dna[i] != design.dna[i]:
            mismatch_5 = i
            break

    for j in itertools.count(1):
        if wt.dna[-j] != design.dna[-j]:
            mismatch_3 = -j + 1
            break

    if verbose:
        print("5' matching region (wt):", wt.dna[:mismatch_5])
        print("5' matching region (design):", design.dna[:mismatch_5])
        print()
        print("mismatched region (wt):", wt.dna[mismatch_5:mismatch_3])
        print("mismatched region (design):", design.dna[mismatch_5:mismatch_3])
        print()
        print("3' matching region (wt):", wt.dna[mismatch_3:])
        print("3' matching region (design):", design.dna[mismatch_3:])
        print()

    wt_5 = wt.dna[:mismatch_5]
    wt_3 = wt.dna[mismatch_3:]
    insert = design.dna[mismatch_5:mismatch_3]

    # Design the part of the primers that will anneal with the wildtype plasmid.

    overlaps_5 = [wt_5[-j:] for j in range(1, len(wt_5))]
    overlap_5, tm_5 = pick_primer_with_best_tm(overlaps_5, tm)

    overlaps_3 = [wt_3[:i] for i in range(1, len(wt_5))]
    overlap_3, tm_3 = pick_primer_with_best_tm(overlaps_3, tm)

    if verbose:
        print("5' overlap:", overlap_5)
        print("5' overlap Tm:", tm_5)
        print("5' overlap GC%:", 100 * sum(x in 'GC' for x in overlap_5) / len(overlap_5))
        print("5' overlap len:", len(overlap_5))
        print()
        print("3' overlap:", overlap_3)
        print("3' overlap Tm:", tm_3)
        print("3' overlap GC%:", 100 * sum(x in 'GC' for x in overlap_3) / len(overlap_3))
        print("3' overlap len:", len(overlap_3))
        print()

    # Design the part of the primers that will contain the aptamer insert.

    if cut is None:
        dlen = len(overlap_5) - len(overlap_3)
        cut = (len(insert) - dlen) // 2

    overhang_5 = insert[:cut].lower()
    overhang_3 = insert[cut:].lower()

    if verbose:
        print("5' overhang:", overlap_5)
        print("3' overhang:", overlap_3)
        print()

    # Combine the two halves of each primer.  Print the overlap in uppercase and 
    # the overhang in lowercase.  Reverse-complement the 5' primer.

    primer_5 = reverse(complement(overlap_5 + overhang_5))
    primer_3 = overhang_3 + overlap_3

    name = design.underscore_name.upper()
    name_5 = name + '_REV'
    name_3 = name + '_FOR'

    return {name_5: primer_5, name_3: primer_3}

def print_cloning_primers(primers):
    print("Number of oilgos:")
    print(len(primers))
    print()
    print("Primer names (ready to copy into Elim form):")
    for name in sorted(primers):
        print(name)
    print()
    print("Primer sequences (ready to copy into Elim form):")
    for name in sorted(primers):
        print(primers[name])

def pick_primer_with_best_tm(seqs, tm):
    import primer3
    seq_tms = [
            (seq, primer3.calcTm(seq, tm_method='breslauer'))
            for seq in seqs
    ]
    seq_tms.sort(key=lambda seq_tm: abs(seq_tm[1] - tm))
    return seq_tms[0]

def reverse(sequence):
    return sequence[::-1]

def complement(sequence):
    complements = {
            'a': 't',
            't': 'a',
            'c': 'g',
            'g': 'c',
            'r': 'y',
            'y': 'r',
            's': 'w',
            'w': 's',
            'k': 'm',
            'm': 'k',
            'b': 'v',
            'v': 'b',
            'd': 'h',
            'h': 'd',
            'n': 'n',

            'A': 'T',
            'T': 'A',
            'C': 'G',
            'G': 'C',
            'N': 'N',
            'R': 'Y',
            'Y': 'R',
            'S': 'W',
            'W': 'S',
            'K': 'M',
            'M': 'K',
            'B': 'V',
            'V': 'B',
            'D': 'H',
            'H': 'D',
            'N': 'N',
    }
    return ''.join(complements[x] for x in sequence)


if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)
    cut = args['--cut'] and int(args['--cut'])
    tm = float(args['--tm'])
    spacer = args['--spacer']
    primers = {}

    for design in args['<designs>']:
        primers.update(design_cloning_primers(design, spacer,
            cut=cut, tm=tm, verbose=args['--verbose']))

    print_cloning_primers(primers)

