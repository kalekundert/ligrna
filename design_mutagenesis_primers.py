#!/usr/bin/env python3

"""\
Design primers for either inverse PCR or Quikchange mutagenesis.

Usage:
    design_mutagenesis_primers.py <name> <backbone> <construct> [options]

Arguments:
    <name>
        A prefix to name the primers with.

    <backbone>
        The DNA sequence of the existing plasmid around the region you want to 
        mutate.  The region you want to mutate must be flanked on either side 
        by ≈40 bp that you don't want to change, so primers can be found.

    <construct>
        The DNA sequence of the existing plasmid with your desired changes 
        included.  This sequence must be exactly the same length as the 
        backbone sequence, and must be start and end with the same fixed 
        sequences, where primers will be found.

Options:
    -q, --quikchange
        Design primers for Quikchange instead of inverse PCR.  Quikchange is 
        slightly easier for point mutations or very small insertions or 
        deletions.
        
    -c, --cut <index>
        Manually specify where the index where the insert should be split, 
        relative to the insert itself.  By default, the cut site is chosen to 
        make the primers the same length.  

    -T, --tm <celsius>
        The desired melting temperature for the primers.  The default is 60°C 
        for inverse PCR primers and 78°C for Quikchange.  (Note that Tm is 
        calculated differently for the two cloning strategies.)

    -v, --verbose
        Show extra debugging output.
"""

class PrimerDesigner:

    def __init__(self):
        self.name = None
        self.construct = None
        self.backbone = None
        self.spacer = None
        self.quikchange = False
        self.cut = None
        self.tm = None
        self.verbose = False

    def design_primers(self):
        if self.quikchange:
            return self.design_quikchange_primers()
        else:
            return self.design_inverse_pcr_primers()

    def design_inverse_pcr_primers(self):
        # Find where the design differs from the wildtype sequence.

        bb_5, insert, _, bb_3 = self.find_mismatch()

        # Design the part of the primers that will anneal with the wildtype 
        # plasmid.

        tm = self.tm if self.tm is not None else 60

        overlaps_5 = [bb_5[-j:] for j in range(1, len(bb_5))]
        overlap_5, tm_5 = pick_primer_with_best_tm(overlaps_5, tm)

        overlaps_3 = [bb_3[:i] for i in range(1, len(bb_3))]
        overlap_3, tm_3 = pick_primer_with_best_tm(overlaps_3, tm)

        if self.verbose:
            print("5' overlap:", overlap_5)
            print("5' overlap Tm:", tm_5)
            print("5' overlap GC%:", gc_percent(overlap_5))
            print("5' overlap len:", len(overlap_5))
            print()
            print("3' overlap:", overlap_3)
            print("3' overlap Tm:", tm_3)
            print("3' overlap GC%:", gc_percent(overlap_3))
            print("3' overlap len:", len(overlap_3))
            print()

        tm_margin = 3
        if abs(tm - tm_5) > tm_margin or abs(tm - tm_3) > tm_margin:
            raise ValueError("Can't design primers for {0.name} with Tm within {1}°C of {0.tm}".format(self, tm_margin))

        # Design the part of the primers that will contain the insert.

        if self.cut is not None:
            cut = self.cut
        elif '/' in insert:
            cut = insert.find('/')
            insert = insert[:cut] + insert[cut+1:]
        else:
            dlen = len(overlap_5) - len(overlap_3)
            cut = (len(insert) - dlen) // 2

        if self.verbose:
            print("cut point:", cut)
            print()

        overhang_5 = insert[:cut]
        overhang_3 = insert[cut:]

        if self.verbose:
            print("5' overhang:", overlap_5)
            print("3' overhang:", overlap_3)
            print()

        # Combine the two halves of each primer.  Print the overlap in uppercase and 
        # the overhang in lowercase.  Reverse-complement the 5' primer.

        primer_5 = reverse(complement(overlap_5.lower() + overhang_5.upper()))
        primer_3 = overhang_3.upper() + overlap_3.lower()

        if self.verbose:
            print("forward primer len:", len(primer_3))
            print("reverse primer len:", len(primer_5))
            print()

        name = self.name.upper()
        if name.startswith('NONE_'): name = name[5:]
        name_5 = name + '_TM_{}_REV'.format(int(tm_5))
        name_3 = name + '_TM_{}_FOR'.format(int(tm_3))

        return {name_5: primer_5, name_3: primer_3}

    def design_quikchange_primers(self):
        # Find where the construct differs from the backbone.

        bb_5, insert, replace, bb_3 = self.find_mismatch()
        bb_5, insert, bb_3 = bb_5.lower(), insert.upper(), bb_3.lower()

        # Make a list of every possible primer that has the insert centered to 
        # within two nucleotides.

        tm = self.tm if self.tm is not None else 78

        primers = []
        max_n = min(len(bb_5), len(bb_3))
        for n in range(max_n):
            for dn in range(-2, 3):
                if n + dn > 0:
                    primers.append(bb_5[-n:] + insert + bb_3[:n+dn])

        if self.verbose:
            print("num possible primers:", len(primers))

        # Discard any primer with a Tm below the given limit.

        primer_tms = {
                primer: calculate_agilent_tm(primer, insert, replace)
                for primer in primers}

        primers = [
                primer for primer in primers
                if primer_tms[primer] >= tm]

        if self.verbose:
            print("num high enough Tm:", len(primers))
            print()

        if not primers:
            raise ValueError("no primers with Tm > {}°C for {}".format(tm, self.name))

        # Score the remaining primers based on how close their Tm is to the 
        # limit, how close their GC% is to 0.4, and whether they start and end 
        # with a 'G' or a 'C'.

        primer_scores = {
                primer: sum([
                    1.0 * abs(tm - primer_tms[primer]),  # Prefer primers with melting temperature close to 78°C.
                    5.0 * abs(0.4 - gc_percent(primer)),  # Prefer primers with about 40% G or C.
                    5.0 * ((primer[0] in 'AT') + (primer[-1] in 'AT')),  # Prefer primers that start and end with G or C.
                    1.0 * max(0, len(primer) - 50),  # Primers longer than 50 bp are more expensive.
                ])
                for primer in primers
        }

        # Pick the primer with the best score.

        by_score = lambda k: primer_scores[k]
        best_primers = sorted(primer_scores.keys(), key=by_score)
        best_primer = best_primers[0]

        if self.verbose:
            print("best primer score:", primer_scores[best_primer])
            print("best primer Tm:", primer_tms[best_primer])
            print("best primer GC%:", gc_percent(best_primer))
            print("best primer len:", len(best_primer))
            print()

        # Construct the forward and reverse primers.

        name = self.name.upper()
        if name.startswith('NONE_'): name = name[5:]
        name_for = name + '_QUIK_FOR'
        name_rev = name + '_QUIK_REV'

        return {name_for: best_primer, name_rev: reverse(complement(best_primer))}

    def find_mismatch(self):
        import itertools

        if self.construct == self.backbone:
            raise ValueError("{} is the same as the backbone.".format(self.name))

        mismatch_5 = None
        mismatch_3 = None

        for i in itertools.count():
            if self.backbone[i] != self.construct[i]:
                mismatch_5 = i
                break

        for j in itertools.count(1):
            if self.backbone[-j] != self.construct[-j]:
                mismatch_3 = -j + 1
                break

        if self.verbose:
            print("5' matching region (construct):", self.construct[:mismatch_5])
            print("5' matching region (backbone):", self.backbone[:mismatch_5])
            print()
            print("mismatched region (construct):", self.construct[mismatch_5:mismatch_3])
            print("mismatched region (backbone):", self.backbone[mismatch_5:mismatch_3])
            print()
            print("3' matching region (construct):", self.construct[mismatch_3:])
            print("3' matching region (backbone):", self.backbone[mismatch_3:])
            print()

        return (self.backbone[:mismatch_5],
                self.construct[mismatch_5:mismatch_3],
                self.backbone[mismatch_5:mismatch_3],
                self.backbone[mismatch_3:])



def configure_primer_designers_from_docopt():
    import docopt
    import shlex
    import sgrna_sensor

    args = docopt.docopt(__doc__)
    default_backbone_name = args['--backbone'] or 'on'
    default_spacer = args['--spacer'] or 'none'
    default_quikchange = args['--quikchange']
    default_cut = args['--cut']
    default_tm = args['--tm']
    default_verbose = args['--verbose']

    for name in args['<constructs>']:
        sub_cli = shlex.split(name)
        sub_args = docopt.docopt(__doc__, sub_cli)

        for sub_name in sub_args['<constructs>']:
            designer = PrimerDesigner()
            designer.name = sub_name
            designer.spacer = sub_args['--spacer'] or default_spacer
            designer.quikchange = sub_args['--quikchange'] or default_quikchange
            designer.cut = int_or_none(sub_args['--cut'] or default_cut)
            designer.tm = float(sub_args['--tm'] or default_tm or \
                    (78 if designer.quikchange else 60))
            designer.verbose = sub_args['--verbose'] or default_verbose

            sgrna = sgrna_sensor.from_name(sub_name, target=designer.spacer)
            designer.name = sgrna.underscore_name
            designer.construct = sgrna.dna
            designer.backbone = sgrna_sensor.from_name(
                    sub_args['--backbone'] or default_backbone_name,
                    target=designer.spacer).dna

            yield designer

def consolidate_duplicate_primers(primers, term_sep='_'):
    from collections import defaultdict
    from natsort import natsorted

    # Find all the names that each primer is referred to by.

    primer_names = defaultdict(list)

    for name, primer in primers.items():
        primer_names[primer].append(name)

    # For primers that have multiple names, make a new name by combining all 
    # the old ones.  The user will be expected to simplify the name when 
    # copying and pasting the primers into the Elim form.

    unique_primers = {}

    for primer, names in primer_names.items():
        name = ', '.join(natsorted(names))
        unique_primers[name] = primer

    return unique_primers
    
def report_primers_for_elim(primers, key=None):
    from natsort import natsorted
    print("Number of oligos:", len(primers))
    print()
    print("Primer names (ready to copy into Elim form):")
    for name in natsorted(primers):
        print(name)
    print()
    print("Primer sequences (ready to copy into Elim form):")
    for name in natsorted(primers):
        print(primers[name])

def pick_primer_with_best_tm(seqs, tm):
    import primer3
    seq_tms = [
            # primer3 seems to produce garbage results if given lowercase 
            # sequences.
            (seq, primer3.calcTm(seq.upper(), tm_method='breslauer'))
            for seq in seqs
    ]
    seq_tms.sort(key=lambda seq_tm: abs(seq_tm[1] - tm))
    return seq_tms[0]

def calculate_agilent_tm(seq, insert, replace):
    """
    Use the Agilent formula to calculate a Tm for the given sequence.  This is 
    the only method that should be used when designing Quikchange primers.
    """
    gc = 100 * gc_percent(seq)
    N = len(seq)
    mismatch = 100 * min(len(insert), len(replace)) / N
    return 81.5 + 0.41*gc - 675/N - mismatch

def reverse(seq):
    return seq[::-1]

def complement(seq):
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
    return ''.join(complements[x] for x in seq)

def gc_percent(seq):
    seq = seq.upper()
    gc = seq.count('G') + seq.count('C')
    return gc / len(seq)

def int_or_none(x):
    return int(x) if x is not None else None

def float_or_none(x):
    return float(x) if x is not None else None


if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)

    designer = PrimerDesigner()
    designer.name = args['<name>']
    designer.backbone = args['<backbone>']
    designer.construct = args['<construct>']
    designer.quikchange = args['--quikchange']
    designer.cut = int_or_none(args['--cut'])
    designer.tm = float_or_none(args['--tm'])
    designer.verbose = args['--verbose']

    primers = designer.design_primers()
    primers = consolidate_duplicate_primers(primers)
    report_primers_for_elim(primers)
