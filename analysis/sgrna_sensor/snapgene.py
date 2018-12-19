#!/usr/bin/env python3

"""\
Usage:
    ./make_ligrna.py <ligrna> [options]

Options:
    -t --template PATH  [default: template.dna]
        The existing snapgene file to copy.  

    -c --spacer-color NAME  [default: grey]
        The color to make the spacer.  The following colors are understood: 
        'red', 'orange', 'lime', 'yellow', 'green', 'teal', 'blue', 'purple', 
        'grey'.  Alternatively, you can provide a hex code in the following 
        format: '#xxxxxx'.

    -d --dry-run
        Display the path that would be created and its corresponding spacer, 
        but don't actually create the file.

"""

import docopt, csv, os
import pyperclip
from sh import cp
from subprocess import call
from . import from_name
from pathlib import Path
from pprint import pprint

colors = {
        'red':      '#ff0000',
        'orange':   '#ff9900',
        'lime':     '#99cc00',
        'yellow':   '#ffff99',
        'green':    '#008000',
        'teal':     '#33cccc',
        'blue':     '#3366ff',
        'purple':   '#cc99ff',
}

def genbank_format(seq):
    from more_itertools import chunked

    genbank = ''
    seq = seq.lower()
    join = lambda x: ''.join(x)
    chunks_60 = map(join, chunked(seq, 60))

    for i, chunk in enumerate(chunks_60):
        chunks_10 = map(join, chunked(chunk, 10))
        genbank += f"""{60 * i + 1:9d} {' '.join(chunks_10)}"""

    return genbank.rstrip()

def main():
    args = docopt.docopt(__doc__)
    ligrna = from_name(args['<ligrna>'])
    spacer = ligrna['spacer']
    spacer_color = colors.get(args['--spacer-color'], args['--spacer-color'])
    ligrna_name = f'{ligrna.abbrev} {",".join(ligrna.args)}'

    genbank = f"""\
LOCUS       Exported                  {len(ligrna)} bp ds-DNA     linear   UNA 31-AUG-2017
REFERENCE   1  (bases 1 to 20)
  AUTHORS   Kale Kundert
  TITLE     Direct Submission
  JOURNAL   Exported Aug 31, 2017 from SnapGene 4.0.3
            http://www.snapgene.com
FEATURES             Location/Qualifiers
     misc_feature    1..{len(spacer)}
                     /label={ligrna.spacer}
                     /note="color: {spacer_color}"
     misc_feature    {len(spacer)+1}..{len(ligrna)}
                     /label={ligrna_name}
                     /note="color: #99ccff; direction: RIGHT"
ORIGIN
{genbank_format(ligrna.dna)}
//
"""
    pyperclip.copy(genbank)

    if args['--dry-run']:
        print("dry run, no files created.")
    else:
        src = args['--template']
        dest = f'{ligrna.underscore_name}.dna'
        cp(src, dest)
        call(['fork', '/opt/gslbiotech/snapgene/snapgene.sh', os.path.abspath(dest)])







