#!/usr/bin/env python
# encoding: utf-8

"""\
Display sequences relevant to the sgRNA sensor project.

Usage:
    sgrna_sensor [options] <names>...

Arguments:
    <names>...
        The name of one or more sequences to show.  The name must correspond to 
        one of the functions in 'sgrna_sensor/design.py', which will be called 
        to generate a sequence.  Typically names consist of two letters, where 
        the first indicates the design strategy and the second indicates the 
        affected domain:

        Strategy Abbreviations      Domain Abbreviations  
        ======================      ====================  
        f: fold                     u: upper stem         
        z: zipper                   l: lower stem
        s: serpentine               b: bulge              
        c: circle                   x: nexus              
        h: hammerhead               h: hairpins           
        r: random

        In some cases these two letters might be followed by a 'v', to indicate 
        a variant of an existing design approach.  Typically, the variant would 
        take a more flexible set of arguments than the original design.

        You can specify arguments to pass to the specified design function.
        Any non-alphanumeric characters (like spaces, dashes, or underscores) 
        in the name will be used to delimit arguments.  For example:
        
        Name        Meaning
        =========   ===========================================================
        wt          The wildtype sgRNA targeting AAVS (the default).
        rfp/wt      The wildtype sgRNA targeting RFP.
        dead        An inactive sgRNA only 2 mutations away from WT.
        cb          The "circle bulge" design.
        tet/cb      The "circle bulge" design with the tetracycline aptamer.
        cb/wo       The "circle bulge" design with the "wo" tuning strategy.
        cb(wo)      Another way to spell "cb/wo"

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

    -z, --library-size
        Calculate the number of variants the given designs have.  Libraries 
        should contain IUPAC codes for degenerate nucleotides (e.g. N).

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

import docopt
import math

from .components import *
from .designs import *
from .helpers import *
from .sequence import *

def from_name(name, **kwargs):
    import re, inspect

    name = name.strip()
    if not name:
        raise ValueError("Can't parse empty name.")

    tokens = re.findall('[a-zA-Z0-9]+', name)

    # If the first token matches the name of one of the known targeting 
    # sequences, use that sequence to build the design.  If the next token 
    # (which would be the first if no targeting sequence was found and the 
    # second otherwise) matches the name of one of the known ligand, use that 
    # ligand's aptamer to build the design.

    if tokens[0] == 'pam':
        kwargs['pam'] = tokens.pop(0)

    try:
        spacer(tokens[0])
    except ValueError:
        pass
    else:
        if 'target' not in kwargs:
            kwargs['target'] = tokens.pop(0)

    try:
        aptamer(tokens[0])
    except ValueError:
        pass
    else:
        if 'ligand' not in kwargs:
            kwargs['ligand'] = tokens.pop(0)

    # The first token after the (optional) aptamer specifies the factory 
    # function to use and must exist in the global namespace. 

    try:
        factory = globals()[tokens[0]]
    except KeyError:
        raise ValueError("No designs named '{}'.".format(tokens[0]))

    # All further tokens are arguments.  Arguments that look like integers need 
    # to be casted to integers.

    def cast_if_necessary(x):  # (no fold)
        try: return int(x)
        except: return x

    args = [cast_if_necessary(x) for x in tokens[1:]]

    # Use keyword arguments passed into this function if the factory knows how 
    # to handle them.  Silently ignore the arguments otherwise.

    argspec = inspect.getargspec(factory)
    known_kwargs = {k:v for k,v in kwargs.items() if k in argspec.args}
    return factory(*args, **known_kwargs)

def predict_fold(design, constraints=False):
    import shlex, re
    from subprocess import Popen, PIPE

    if constraints:
        cmd = 'RNAfold --noPS --MEA'
        stdin = design.rna

        # Look for aptamer domains in the given design.

        try:
            aptamer = design['aptamer']
            aptamer_seq = aptamer.rna
            aptamer_fold = aptamer.constraints

            if not hasattr(aptamer, 'kd'):
                raise ValueError("This aptamer does not specify an affinity.")

            aptamer_kd = aptamer.kd

        # If no aptamer domains are found, look specifically for the 
        # theophylline aptamer.  The theophylline aptamer cannot be recognized 
        # by the above code because it's got too much backwards-compatibility 
        # baggage, but it's important enough to merit a special case.

        # Note that this will only give a reasonable answer if the design in 
        # question has the theophylline aptamer flanked by a valid base pair 
        # (e.g. GC, AU, GU).  The folding simulation won't complain if this 
        # condition isn't met, but it will give the wrong answer.

        except KeyError:
            theo_pattern = re.compile('.AUACCAGCCGAAAGGCCCUUGGCAG.')
            theo_match = theo_pattern.search(design.rna)

            if not theo_match:
                raise ValueError('No aptamer in {}.'.format(design.name))

            aptamer_seq = theo_match.group()
            aptamer_fold = '(...((.(((....)))....))...)'
            aptamer_kd = 0.0324  # μM

        # Calculate the free energy of aptamer folding.
        rt_37 = 1.9858775e-3 * 310  # kcal/mol at 37°C
        std_conc = 1e6  # 1M in μM
        aptamer_dg = rt_37 * math.log(aptamer_kd / std_conc)

        # Add the aptamer motif to RNAfold.
        cmd += ' --motif "{},{},{}"'.format(
                aptamer_seq, aptamer_fold, aptamer_dg)

        # Show the user how the aptamer is being scored.
        aptamer_start = design.rna.find(aptamer_seq)
        print(' ' * aptamer_start, end='')
        print(aptamer_fold, end='')
        print(' ' * (len(design) - aptamer_start - len(aptamer_seq)), end=' ')
        print("({:.2f} kcal/mol)".format(aptamer_dg))

    else:
        cmd = 'RNAfold --noPS --MEA'
        stdin = design.rna

    process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(stdin.encode())
    return '\n'.join(
        x for x in stdout.decode().split('\n')[1:]
        if not x.startswith('WARNING')).strip()

def molecular_weight(name, polymer='rna'):
    return from_name(name).mass(polymer)

def main():
    args = docopt.docopt(__doc__)
    designs = []

    kwargs = {}
    if args['--spacer']:
        kwargs['target'] = args['--spacer']
    if args['--no-spacer']:
        kwargs['target'] = None

    for name in args['<names>']:
        design = from_name(name, **kwargs)
        designs.append(design)

    if args['--batch']:
        args['--t7'] = True
    if args['--t7']:
        args['--dna'] = True

    format_args = {  # (no fold)
            'color': args['--color'],
            'rna': True,    # Overridden if 'dna' is True.
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

    for design in designs:
        if args['--verbose']:
            from textwrap import dedent
            header = "{}".format(design.name)
            print()
            print(header)
            print('=' * len(header))
            if design.doc:
                print(dedent(design.doc).strip())
                print()
                print("Sequence")
                print("--------")

        if args['--t7']:
            if design['spacer'] == '':
                print("'{}' does not have a spacer sequence, refusing to add T7 promoter.".format(design.name))
                continue
            design.prepend(t7_promoter())

        if args['--pretty']:
            print(header_template.format(design.name), end='  ')
            design.show(labels=True, **format_args)

        elif args['--batch']:
            print(header_template.format(design.underscore_name), end='\t')
            design.show(labels=False, **format_args)

        elif args['--fasta']:
            print('>' + design.name)
            format_args['color'] = 'never'
            design.show(labels=False, **format_args)

        elif args['--library-size']:
            print(header_template.format(design.name), end='  ')
            z = library_size(design.seq)
            print('{}  (4**{})'.format(z, math.log(z)/math.log(4)))

        elif args['--length']:
            print(header_template.format(design.name), end='  ')
            print(len(design))

        elif args['--rnafold']:
            design.show(labels=False, rna=True, color=args['--color'])
            print(predict_fold(design))

            if args['--constraints']:
                print()
                design.show(labels=False, rna=True, color=args['--color'])
                print(predict_fold(design, True))

            if design is not designs[-1]:
                print()

        else:
            design.show(labels=False, **format_args)

