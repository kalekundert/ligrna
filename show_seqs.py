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

Options:
    -d, --dna
        Show the DNA sequence for the specified design instead of the RNA 
        sequence.

    -t, --t7
        Append the T7 promoter sequence to the design.  This options 
        automatically enables the '--dna' option.

    -s, --spacer TARGET     [default: aavs]
        Specify the sequence that the sgRNA should target.  If an empty string 
        is given, no spacer sequence will be included.

    -a, --aptamer NAME      [default: theo]
        Specify the aptamer that should be inserted into the sgRNA.

    -S, --subset RANGE
        Specify a subset of the design to display.  If only one number is 
        given, it is taken as the start position.  If two numbers are given, 
        separated by a colon, they are taken as the start and end positions.  
        If the subset starts with an underscore, the sequence will be padded.

    -p, --pretty
        Include pretty names and the "5'-" and "-3'" labels for each design.

    -b, --batch
        Prepare sequences for batch processing.  Use a more simple character 
        set for the names, automatically append the T7 sequence, and don't 
        display the "5'-" and "-3'" labels.
        
    -r, --rnafold
        Run each design through RNAfold and display the resulting secondary 
        structure prediction.  If the '--constraints' flag is given, any base 
        pairing constraints associated with each design are passed to RNAfold.  

    -c, --constraints
        If RNA secondary structure is being calculated, calculate it with any 
        relevant constraints.  Typically restraints are used to force aptamers 
        to adopt their bound conformation.

    -C, --color=WHEN    [default: auto]
        Specify whether or not the sequences should be colored according to 
        their architectural role in the design.
        
"""

import sgrna_helper
import docopt

args = docopt.docopt(__doc__)
designs = []

kwargs = {}
kwargs['target'] = args['--spacer'] or None
kwargs['small_molecule'] = args['--aptamer']

for name in args['<names>']:
    try:
        design = sgrna_helper.from_name(name, **kwargs)
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

if args['--subset']:
    int_or_none = lambda x: int(x) if x else None

    if args['--subset'].startswith('_'):
        format_args['pad'] = True
        args['--subset'] = args['--subset'][1:]
    if ':' in args['--subset']:
        format_args['start'] = int_or_none(args['--subset'].split(':')[0])
        format_args['end'] = int_or_none(args['--subset'].split(':')[1])
    else:
        format_args['start'] = int(args['--subset'])

longest_name = max([8] + [len(x.name) for x in designs])
header_template = '{{0:{}s}}'.format(longest_name)

for design in designs:
    if args['--t7'] or args['--batch']:
        design.prepend(sgrna_helper.t7_promoter())

    if args['--pretty']:
        print(header_template.format(design.name), end='  ')
        design.show(labels=True, **format_args)
    elif args['--batch']:
        print(header_template.format(design.underscore_name), end='\t')
        design.show(labels=False, **format_args)
    elif args['--rnafold']:
        from subprocess import Popen, PIPE; import shlex
        design.show(labels=False, rna=True, color=args['--color'])
        if args['--constraints']:
            cmd = 'RNAfold --noPS --MEA -C'
            stdin = design.rna + '\n' + design.constraints 
            print(design.constraints, '(constraints)')
        else:
            cmd = 'RNAfold --noPS --MEA'
            stdin = design.rna
        process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE)
        stdout, stderr = process.communicate(stdin.encode())
        print('\n'.join(stdout.decode().split('\n')[1:]).strip())
    else:
        design.show(labels=False, **format_args)


