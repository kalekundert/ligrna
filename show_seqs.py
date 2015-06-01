#!/usr/bin/env python3

"""\
Display sequences relevant to the sgRNA sensor project.

Usage:
    show_designs.py [options] <names>...

Arguments:
    <names>...
        The name of one or more sequences to show.  The name must correspond to 
        a function in 'sgrna_helper.py', which will be called to generate the 
        sequence to show.  You can specify arguments to pass to that function.  
        Any non-alphanumeric characters (like spaces, dashes, or underscores) 
        in the name will be used to delimit arguments.  For example:
        
        Name        Meaning
        =========   ===========================================================
        wt          The wildtype sgRNA sequence targeting AAVS (the default).
        wt_rfp      The wildtype sgRNA sequence targeting RFP.
        dead        An inactive sgRNA sequence only 2 mutations away from WT.
        t7          The T7 promoter sequence.
        theo        The theophylline aptamer sequence.
        aavs        The AAVS target sequence.
        us_0_0      The upper stem insertion design with parameters N=0, l=0.
        us-0-0      Same as above.
        us(0,0)     Same as above.
        ls_6_2      The lower stem insertion design with parameters N=6, l=2.
        nx_3        The nexus insertion design with parameters l=3.
        hp_18       The hairpin replacement design with parameters N=18.

        You can also use a plus sign to concatenate two or more sequences.  
        This is most often useful for prepending a T7 promoter onto another 
        sequence.  For example:

        Name        Meaning
        =========   ===========================================================
        t7+wt       The wildtype sgRNA sequence with the T7 promoter added.
        t7+us_0_0   The specified upper stem design with the T7 promoter added.

Options:
    -d, --dna
        Show the DNA sequence for the specified design instead of the RNA 
        sequence.

    -t, --t7
        Append the T7 promoter sequence to the design.  This options 
        automatically enables the '--dna' option.

    -r, --range RANGE
        Specify a subset of the design to display.  If only one number is 
        given, it is taken as the start position.  If two numbers are given, 
        separated by a colon, they are taken as the start and end positions.  
        If the range starts with an underscore, the sequence will be padded.

    -b, --batch
        Prepare sequences for batch processing.  Use a more simple character 
        set for the names, automatically append the T7 sequence, and don't 
        display the "5'-" and "-3'" labels.
        
    -s, --sequence-only
        Don't show anything but the sequence for each design.

    -c, --color=WHEN    [default: auto]
        Specify whether or not the sequences should be colored according to 
        their architectural role in the design.
        
"""

import sgrna_helper
import docopt

args = docopt.docopt(__doc__)
designs = []

for name in args['<names>']:
    try:
        design = sgrna_helper.from_name(name)
        designs.append(design)
    except ValueError as error:
        print(error)

if args['--batch']:
    args['--t7'] = True
if args['--t7']:
    args['--dna'] = True

format_args = {  # (no fold)
        'color': args['--color'],
        'dna': args['--dna'],
        'pad': False,
}

if args['--range']:
    int_or_none = lambda x: int(x) if x else None

    if args['--range'].startswith('_'):
        format_args['pad'] = True
        args['--range'] = args['--range'][1:]
    if ':' in args['--range']:
        format_args['start'] = int_or_none(args['--range'].split(':')[0])
        format_args['end'] = int_or_none(args['--range'].split(':')[1])
    else:
        format_args['start'] = int(args['--range'])

longest_name = max([8] + [len(x.name) for x in designs])
header_template = '{{0:{}s}}'.format(longest_name)

for design in designs:
    if args['--t7'] or args['--batch']:
        design = design.prepend(sgrna_helper.t7_promoter())

    if args['--batch']:
        print(header_template.format(design.underscore_name), end='\t')
        design.show(labels=False, **format_args)
    elif args['--sequence-only']:
        design.show(labels=False, **format_args)
    else:
        print(header_template.format(design.name), end='  ')
        design.show(**format_args)


