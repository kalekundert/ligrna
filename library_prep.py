#!/usr/bin/env python3
# encoding: utf-8

"""\
Usage:
    library_prep.py <num_libraries> <annealing_temp> [<vector>] [options]

Arguments:
    <num_libraries>
        The number of libraries to construct.  This affects the master mix 
        volumes calculated at various steps.

    <annealing_temp>
        The annealing temperature for the inverse PCR reaction.

    <vector>                        [default: pBLO]
        The vector that you're cloning the library into.  This affects default 
        values for some of the other parameters, most notably the extension 
        time (for the inverse PCR reaction).

Options:
    -r --reaction-volume <μL>       [default: 50]
        The volume of each PCR reaction.

    -p --primer-conc <μM>           [default: 200]
        The concentration of the primers.

    -x --extension-time <secs>
        The length of the annealing step in seconds.  The rule of thumb is 30 
        sec/kb, perhaps longer if you're amplifying a whole plasmid.

    -t --top10-only
        Stop after the Top10 electrotransformation.

    -v --verbose
        Include extra steps such as how to order primers.
"""

import docopt
import dirty_water
import nonstdlib

protocol = dirty_water.Protocol()

## Parse arguments

args = docopt.docopt(__doc__)
num = int(eval(args['<num_libraries>']))
N = nonstdlib.plural(num)

if args['<vector>'] in ('pan', 'pAN'):
    args['--extension-time'] = args['--extension-time'] or '4:00'
    args['--top10-only'] = True
else: # pBLO
    args['--extension-time'] = args['--extension-time'] or '2:00'

## Primer design

if args['--verbose']:
    protocol += """\
Design primers to assemble the {N:/library/libraries} with.

- The ``clone_into_wt.py`` script can design these 
  primers automatically.

- The primers should have overhangs containing the 
  degenerate nucleotides that make up the library.

- The complementarity between the primers and the 
  plasmid should have a Tm near 60°C.

- Order the 5' phosphate modification for the 
  primers.
  
- You can also order HPLC/PAGE purification if 
  your primers are long and you don't mind the 
  extra expense, but the regular purification 
  worked well for me."""

## Inverse PCR

def time_to_secs(time): #
    if ':' in time:
        min, sec = map(int, time.split(':'))
        return 60 * min + sec
    else:
        # Assume the time is just a number of seconds.
        return int(time)

pcr = dirty_water.Pcr()
pcr.num_reactions = num
pcr.annealing_temp = args['<annealing_temp>']
pcr.extension_time = time_to_secs(args['--extension-time'])
pcr.make_primer_mix = True
pcr.reaction.volume = eval(args['--reaction-volume'])
pcr.primer_mix['forward primer'].stock_conc = float(args['--primer-conc'])
pcr.primer_mix['reverse primer'].stock_conc = float(args['--primer-conc'])

protocol += pcr

## DpnI digestion

protocol += """\
Add 1 μL (20 units) DpnI to each reaction and 
incubate at 37°C for 1h."""

## PCR cleanup

protocol += """\
Run a gel to confirm that the product is clean.  
If it is, purify it using a PCR cleanup kit.  If 
it isn't, either optimize the reaction or (for 
small libraries) gel extract the desired band."""

## Ligation

lig_rxn = dirty_water.Reaction('''\
Reagent                Conc  Each Rxn  Master Mix
================  =========  ========  ==========
PCR product       ≈30 ng/μL  50.00 μL
T4 ligase buffer        10x   5.67 μL
T4 ligase          400 U/μL   1.00 μL
''')
lig_rxn.show_master_mix = False

protocol += """\
Setup {num} ligation {N:reaction/s}.

{lig_rxn}"""

protocol += """\
Incubate overnight at 16°C."""

## Top10 transformation

protocol += """\
Desalt and concentrate the ligated DNA using a 
Zymo spin column with the Qiagen buffers:

- Add 285 μL PB to the ligation reaction.

- Transfer to a Zymo spin column.

- Wash with 200 μL PE.

- Wash with 200 μL PE again.

- Elute in 10 μL water."""

protocol += """\
Transform the ligated DNA into Top10 cells by 
electroporation.  For each transformation:

- Pre-warm 1 mL SOC and an LB + Carb plate.

- Chill an electroporation cuvette and 2 μL 
  (≈250 ng) of DNA on ice.  

- Thaw an aliquot of competent cells on ice for 
  ~10 min.

- Pipet once to mix the cells with the DNA, then 
  load into the cuvette.  Tap to remove bubbles.

- Shock at 1.8 kV with a 5 ms decay time (for 
  cuvettes with a 1 mm gap).

- Immediately add 1 mL pre-warmed SOC.  If you're 
  transforming multiple aliquots of cells with the 
  same DNA, combine them.

- Before recovering, plate several 10x dilutions 
  of cells (e.g. from 10⁻³ to 10⁻⁶) to count how 
  many were transformed.

- Recover at 37°C for 1h.
  
- Transfer cells to 50 mL selective media and 
  grow overnight at 37°C."""

if args['--top10-only']:
    print(protocol)
    raise SystemExit

## Miniprep

protocol += """\
Miniprep to isolate library plasmid.

- Make a glycerol stock.

- Miniprep 4 mL of overnight culture.

- Do a phenol-chloroform extraction on the lysate 
  after pelleting the insoluble cell debris and 
  before loading it onto the miniprep column.  
  This extra step modestly improves transformation 
  efficiency and isn't necessary for libraries 
  with fewer than 11 randomized positions.

- Elute in 30 μL water."""

protocol += """\
If necessary, combine libraries in proportion to 
the number of unique members in each."""

## MG1655 transformation

protocol += """\
Transform the combined library into MG1655 cells 
by electroporation.

- Use the same transformation protocol described
  above.

- It's best to do the transformation immediately, 
  so as much of the DNA as possible will be 
  supercoiled.  With MG1655 (but not Top10)
  cells, I find that supercoiled DNA gives 100x
  more transformants than relaxed DNA."""

## Glycerol stock

protocol += """\
Store the library as a glycerol stock.

- 333 μL 80% glycerol, 1 mL overnight culture.

- Place at -80°C without snap-freezing."""


print(protocol)

# vim: tw=50
