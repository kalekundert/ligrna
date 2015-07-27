#!/usr/bin/env python3

"""\
Usage: sgrna_to_300nM.py <name> <ng_uL>
"""

if __name__ == '__main__':
    import sys; sys.path.append('../scripts')
    import docopt
    import sgrna_helper

    args = docopt.docopt(__doc__)
    sgrna = sgrna_helper.from_name(args['<name>'])
    ng_uL = float(args['<ng_uL>'])
    nM = ng_uL * 1e6 / sgrna.mass('rna')

    print('{:.2f} nM'.format(nM))

