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

    -t, --table
        Report the primers in a tab-separated table.

    -v, --verbose
        Show extra debugging output.
"""

from sgrna_sensor import primers

if __name__ == '__main__':
    import docopt
    args = docopt.docopt(__doc__)

    designer = primers.PrimerDesigner()
    designer.name = args['<name>']
    designer.backbone = args['<backbone>']
    designer.construct = args['<construct>']
    designer.quikchange = args['--quikchange']
    designer.cut = primers.int_or_none(args['--cut'])
    designer.tm = primers.float_or_none(args['--tm'])
    designer.verbose = args['--verbose']

    results = designer.design_primers()
    results = primers.consolidate_duplicate_primers(results)

    if args['--table']:
        primers.report_primers_to_table(results)
    else:
        primers.report_primers_for_elim(results)
