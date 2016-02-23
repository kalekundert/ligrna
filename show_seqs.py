#!/usr/bin/env python3
# encoding: utf-8

"""\
Display sequences relevant to the sgRNA sensor project.

Usage:
    show_designs.py [options] <names>...

Arguments:
    <names>...
        The name of one or more sequences to show.  The name must correspond to 
        a function in 'sgrna_sensor.py', which will be called to generate the 
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
    -v, --verbose
        Print out a description of the design goals behind each design, along 
        with their sequences.

    -d, --dna
        Show the DNA sequence for the specified design instead of the RNA 
        sequence.

    -t, --t7
        Append the T7 promoter sequence to the design.  This options 
        automatically enables the '--dna' option.

    -s, --spacer TARGET
        Specify the sequence that the sgRNA should target.  If an empty string 
        is given, no spacer sequence will be included.

    -S, --no-spacer
        Specify that the spacer sequence should be left out.  This is just 
        shorthand for "-s ''".

    -i, --slice RANGE
        Specify a subset of the design to display.  If only one number is 
        given, it is taken as the start position.  If two numbers are given, 
        separated by a colon, they are taken as the start and end positions.  
        If the slice starts with an underscore, the sequence will be padded.

    -p, --pretty
        Include pretty names and the "5'-" and "-3'" labels for each design.

    -b, --batch
        Prepare sequences for batch processing.  Use a more simple character 
        set for the names, automatically append the T7 sequence, and don't 
        display the "5'-" and "-3'" labels.

    -f, --fasta
        Display (DNA) sequences in the FASTA format.  T7 promoters are not 
        appended unless the --t7 flag is also given.

    -l, --length
        Show how long a design is, counting only the RNA, not the T7 promoter.
        
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

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sgrna_sensor
import docopt

args = docopt.docopt(__doc__)
designs = []

kwargs = {}
if args['--spacer']:
    kwargs['target'] = args['--spacer']
if args['--no-spacer']:
    kwargs['target'] = None

for name in args['<names>']:
    design = sgrna_sensor.from_name(name, **kwargs)
    designs.append(design)

if args['--batch']:
    args['--t7'] = True
if args['--t7']:
    args['--dna'] = True

format_args = {  # (no fold)
        'color': args['--color'],
        'dna': args['--dna'] or args['--fasta'],
        'pad': False,
}

if args['--slice']:
    int_or_none = lambda x: int(x) if x else None

    if args['--slice'].startswith('_'):
        format_args['pad'] = True
        args['--slice'] = args['--slice'][1:]
    if ':' in args['--slice']:
        format_args['start'] = int_or_none(args['--slice'].split(':')[0])
        format_args['end'] = int_or_none(args['--slice'].split(':')[1])
    else:
        format_args['start'] = int(args['--slice'])

longest_name = max([8] + [len(x.name) for x in designs])
header_template = '{{0:{}s}}'.format(longest_name)

def rnafold(design, constraints=False):
    from subprocess import Popen, PIPE; import shlex
    design.show(labels=False, rna=True, color=args['--color'])
    if constraints:
        cmd = 'RNAfold --noPS --MEA -C'
        stdin = design.rna + '\n' + design.constraints 
        print(design.constraints, '(constraints)')
    else:
        cmd = 'RNAfold --noPS --MEA'
        stdin = design.rna
    process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(stdin.encode())
    print('\n'.join(
        x for x in stdout.decode().split('\n')[1:]
        if not x.startswith('WARNING')).strip())


for design in designs:
    if args['--verbose']:
        from textwrap import dedent
        header = "{}".format(design.name)
        no_doc_message = "No description available for this design."
        print()
        print(header)
        print('=' * len(header))
        print(dedent(design.doc or no_doc_message).strip())
        print()
        print("Sequence")
        print("--------")
    if args['--t7']:
        design.prepend(sgrna_sensor.t7_promoter())

    if args['--pretty']:
        print(header_template.format(design.name), end='  ')
        design.show(labels=True, **format_args)
    elif args['--batch']:
        print(header_template.format(design.underscore_name), end='\t')
        design.show(labels=False, **format_args)
    elif args['--fasta']:
        print('> ' + design.name)
        design.show(labels=False, **format_args)
    elif args['--length']:
        print(header_template.format(design.name), end='  ')
        print(len(design))
    elif args['--rnafold']:
        rnafold(design)
        if args['--constraints']:
            print()
            rnafold(design, True)
    else:
        design.show(labels=False, **format_args)


