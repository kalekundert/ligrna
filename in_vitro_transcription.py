#!/usr/bin/env python3

"""\
Display a protocol for running the given number of in vitro transcription 
reactions.

Usage:
    ./in_vitro_transcription.py <reactions> [options]

Options:
    -d --dna MICROLITERS    [default: 1.0]
        How much template DNA to use (in μL).

    -k --kit BRAND   [default: hiscribe]
        Which in vitro transcription kit to use.  Valid options are 'hiscribe'
        and 'ampliscribe'.

    -i --incubate HOURS
        How long to incubate the transcription reaction.  The default depends
        on which kit you're using.

    -x --extra PERCENT      [default: 10]
        How much extra master mix to create.

    -R --no-rntp-mix
        Indicate that each you're not using a rNTP mix and that you need to add 
        each rNTP individually to the reaction.

    -c --cleanup METHOD     [default: zymo]
        Choose the method for removing free nucleotides from the RNA:
        'none': Carry on the crude reaction mix.
        'zymo': Zymo spin kits.
        'ammonium': Ammonium acetate precipitation.

    -g --gel
        Print detailed instructions on how to do RNA PAGE.
"""

import docopt
import dirty_water
from nonstdlib import plural

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()

## Calculate reagent volumes.

ivtt = dirty_water.Reaction()
ivtt.num_reactions = eval(args['<reactions>'])
ivtt.extra_master_mix = float(args['--extra'])
dna = float(args['--dna'])

if 'hiscribe'.startswith(args['--kit'].lower()):
    incubation_time = args['--incubate'] or 4
    incubation_temp = '37'

    # For short RNA transcripts (< 0.3 kb), we can use less buffer, rNTPs, and 
    # polymerase than usual.  The "10x" concentrations in the reagent table 
    # below are what's printed on the tubes and are relative to the normal 
    # reaction, but maybe confusing unless you keep in mind that our final 
    # concentrations will be 0.75x.

    ivtt['nuclease-free water'].std_volume = 11 - dna, 'μL'
    ivtt['nuclease-free water'].master_mix = True
    ivtt['reaction buffer'].std_volume = 1.5, 'μL'
    ivtt['reaction buffer'].std_stock_conc = '"10x"'
    ivtt['reaction buffer'].master_mix = True

    if args['--no-rntp-mix']:
        ivtt['ATP'].std_volume = 1.5, 'μL'
        ivtt['ATP'].master_mix = True
        ivtt['ATP'].std_stock_conc = 100, 'mM'
        ivtt['CTP'].std_volume = 1.5, 'μL'
        ivtt['CTP'].master_mix = True
        ivtt['CTP'].std_stock_conc = 100, 'mM'
        ivtt['GTP'].std_volume = 1.5, 'μL'
        ivtt['GTP'].master_mix = True
        ivtt['GTP'].std_stock_conc = 100, 'mM'
        ivtt['UTP'].std_volume = 1.5, 'μL'
        ivtt['UTP'].master_mix = True
        ivtt['UTP'].std_stock_conc = 100, 'mM'
    else:
        ivtt['rNTP mix'].std_volume = 6.0, 'μL'
        ivtt['rNTP mix'].std_stock_conc = 100, 'mM'
        ivtt['rNTP mix'].master_mix = True

    ivtt['HiScribe T7 (NEB)'].std_volume = 1.5, 'μL'
    ivtt['HiScribe T7 (NEB)'].std_stock_conc = '"10x"'
    ivtt['HiScribe T7 (NEB)'].master_mix = True
    ivtt['DNA template'].std_volume = dna, 'μL'
    ivtt['DNA template'].std_stock_conc = 10, 'ng/μL'

elif 'ampliscribe'.startswith(args['--kit'].lower()):
    incubation_time = args['--incubate'] or 1
    incubation_temp = '42'

    ivtt['nuclease-free water'].std_volume = 6.3 - dna, 'μL'
    ivtt['nuclease-free water'].master_mix = True
    ivtt['reaction buffer'].std_volume = 2.0, 'μL'
    ivtt['reaction buffer'].std_stock_conc = '10x'
    ivtt['reaction buffer'].master_mix = True

    if args['--no-rntp-mix']:
        ivtt['ATP'].std_volume = 1.8, 'μL'
        ivtt['ATP'].std_stock_conc = 100, 'mM'
        ivtt['ATP'].master_mix = True
        ivtt['CTP'].std_volume = 1.8, 'μL'
        ivtt['CTP'].std_stock_conc = 100, 'mM'
        ivtt['CTP'].master_mix = True
        ivtt['GTP'].std_volume = 1.8, 'μL'
        ivtt['GTP'].std_stock_conc = 100, 'mM'
        ivtt['GTP'].master_mix = True
        ivtt['UTP'].std_volume = 1.8, 'μL'
        ivtt['UTP'].std_stock_conc = 100, 'mM'
        ivtt['UTP'].master_mix = True
    else:
        ivtt['rNTP mix'].std_volume = 7.2, 'μL'
        ivtt['rNTP mix'].std_stock_conc = 100, 'mM'
        ivtt['rNTP mix'].master_mix = True

    ivtt['DTT'].std_volume = 2.0, 'μL'
    ivtt['DTT'].std_stock_conc = 100, 'mM'
    ivtt['DTT'].master_mix = True
    ivtt['RiboGuard RNase innhibitor'].std_volume = 0.5, 'μL'
    ivtt['RiboGuard RNase innhibitor'].std_stock_conc = '40x'
    ivtt['RiboGuard RNase innhibitor'].master_mix = True
    ivtt['Ampliscribe T7 (Epicentre)'].std_volume = 2.0, 'μL'
    ivtt['Ampliscribe T7 (Epicentre)'].std_stock_conc = '10x'
    ivtt['Ampliscribe T7 (Epicentre)'].master_mix = True
    ivtt['DNA template'].std_volume = dna, 'μL'
    ivtt['DNA template'].std_stock_conc = 10, 'ng/μL'

else:
    print("Unknown in vitro transcription kit: '{}'".format(args['--kit']))
    print("Known kits are: 'hiscribe' or 'ampliscribe'")
    raise SystemExit

## Clean your bench

protocol += """\
Wipe down your bench and anything you'll touch (e.g. 
pipets, racks, pens, etc.) with RNaseZap."""

## In vitro transcription

protocol += """\
Setup {:? in vitro transcription reaction/s} by mixing
the following reagents at room temperature in the
order given.

{}""".format(
        plural(ivtt.num_reactions), ivtt)

protocol += """\
Incubate at {}°C (thermocycler) for {:? hour/s}.""".format(
    incubation_temp, plural(incubation_time))

## Purify product

if args['--cleanup'] == 'zymo':
    protocol += """\
Remove unincorporated ribonucleotides using Zymo RNA 
Clean & Concentrator 25 spin columns."""

elif args['--cleanup'] == 'ammonium':
    protocol += """\
Remove unincorporated ribonucleotides using
ammonium acetate precipitation.

Note that ammonium acetate precipitation only works 
for constructs that are longer than 100 bp.

Ammonium Acetate Precipitation
──────────────────────────────
a. Add 1 volume (20 μL) 5M ammonium acetate to 
   each reaction.

b. Incubate on ice for 15 min.

c. Centrifuge at >10,000g for 15 min at 4°C.

d. Wash pellet with 70% ethanol.

e. Dissolve pellet in 20μL nuclease-free water."""

elif args['--cleanup'] == 'none':
    raise SystemExit

else:
    raise ValueError("unknown RNA clean-up method: '{}'".format(args['--cleanup']))

## Nanodrop concentration

protocol += """\
Nanodrop to determine the RNA concentration."""

## Gel electrophoresis

if not args['--gel']:
    protocol += """\
Run the RNA on a denaturing gel to make sure it's 
homogeneous and of the right size."""

else:
    protocol += """\
Run the RNA on a denaturing gel to make sure it's 
homogeneous and of the right size.

- Setup a gel cast and make sure it doesn't leak.
  
- Combine the following reagents in a 15 mL tube and 
  mix until the urea dissolves (~5 min).

  8% TBE/urea polyacrylamide gel
  ──────────────────────────────
  4.2 g urea
  2.0 mL 5x TBE
  2.67 mL 30% acrylamide/bis (29:1)
  water to 10 mthe

- Add 10 uL TEMED and 10 μL 0.4 mg/μL APS (freshly 
  prepared), invert once or twice to mix, then 
  immediately pipet into the gel cast.

- Let the gel set for 1h.
  
- Either use the gel immediately, or wrap it in a
  wet paper towel and store at 4°C overnight to use 
  the next day.
  
To run the gel:

- Mix 2 μL of RNA with 2 μL of loading dye.

- Denature at 95°C for 2 min.

- Wash out any urea that's leached into the wells, 
  then quickly load all of the samples.

- Run at 180V for 30 min.
  
- Soak in 3x GelRed for ~15 min to stain."""

## Aliquot

protocol += """\
Dilute (if desired) enough sgRNA to make several 
15 μL aliquots.  Keep any left-over RNA undiluted.  
Flash-freeze in liquid N₂ and store at -80°C."""


print(protocol)

# vim: tw=53
