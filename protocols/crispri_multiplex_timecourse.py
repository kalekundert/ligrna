#!/usr/bin/env python3

from pprint import pprint

timecourses = [
        ['apo', 'theo', '3mx', 'theo', '3mx'],
        ['apo', 'theo', 'theo+3mx', 'apo', 'theo', 'theo+3mx'],
]
longest_timecourse = max(len(x) for x in timecourses)
shortest_timecourse = min(len(x) for x in timecourses)

def media(media):
    num_cultures = 3
    num_replicates = 3
    num_uses = sum(x.count(media) for x in timecourses)

    volume = num_cultures * num_replicates * num_uses
    volume = 1.2 * volume  # Make 20% extra to be safe.
    volume = 6 * (volume // 6 + 1)  # Round up to the next multiple of 5.

    if media == 'apo':
        ligands = [
                f"  {volume/15:.1f} mL 72 mM NaOH",
        ]
    elif media == 'theo+3mx':
        ligands = [
                f"  {volume/30:.1f} mL 30 mM theo (in 72 mM NaOH)",
                f"  {volume/30:.1f} mL 30 mM 3mx (in 72 mM NaOH)",
        ]
    else:
        ligands = [
                f"  {volume/30:.1f} mL 30 mM {media} (in 72 mM NaOH)",
                f"  {volume/30:.1f} mL 30 mM 72 mM NaOH",
        ]

    return '\n'.join([
              f"{media} media",
            f"  {'─' * (len(media) + 6)}",
            f"  {volume/2:.1f} mL 2x EZ media",
            *ligands,
            f"  {volume - volume/2 - volume/15:.1f} mL water",
            f"  sterile filter",
    ])

def block(i):
    media = []
    num_media = min(i+1, 3)

    for j in range(num_media):
        timepoint = i - j
        row = 'ABC'[j]

        if timepoint < shortest_timecourse \
                and timecourses[0][timepoint] == timecourses[1][timepoint]:
            media.append((f'{row}1-{row}6', timecourses[0][timepoint]))
        else:
            if timepoint < len(timecourses[0]):
                media.append((f'{row}1-{row}3', timecourses[0][timepoint]))
            if timepoint < len(timecourses[1]):
                media.append((f'{row}4-{row}6', timecourses[1][timepoint]))

    return '\n'.join([
        f'  block #{i+1}:',
        *['    {0}: 1 mL {1} media'.format(*x) for x in media],
        '',
    ])

def step(i):
    days = 'Thursday', 'Friday', 'Saturday'
    times = '8:00 AM', '4:00 PM', '12:00 AM'
    date = f'{days[i//3]}, {times[i%3]}'

    harvests = []
    num_harvests = min(i, 3)

    for j in range(num_harvests):
        timepoint = i - j - 1
        if timepoint < longest_timecourse:
            harvests.append((
                f'block #{i}', 'ABC'[j],
                f'plate #{j+1}', 'ABCDEFGH'[timepoint],
            ))

    harvest_table = '\n'.join([
          '────────────────────────────────',
        '  Source             Destination  ',
        '  Block     Row      Plate     Row',
        '  ────────────────────────────────',
        *['  {0:8s}  {1:3s}      {2:8s}  {3:3s}'.format(*x) for x in harvests],
        '  ────────────────────────────────',
    ])

    cultures = []
    num_cultures = min(i+1, 3)

    for j in range(num_cultures):
        cultures.append((
            'ABC'[j],
            f'block #{i}' if i != j else 'overnights',
            f'block #{i+1}',
        ))

    culture_table = '\n'.join([
          '────────────────────────────────',
        '  Row  Source          Destination',
        '  ────────────────────────────────',
        *['  {0:3s}  {1:14s}  {2:11s}'.format(*x) for x in cultures],
        '  ────────────────────────────────',
    ])

    title = f"""\
{date}
{'=' * len(date)}
""" #
    harvest_step = f"""\
- Harvest cells for flow cytometry:

  Pipet 0.5 μL from the indicated row in the source 
  block to the indicated row in the destination plate 
  (which should already contain 250 μL PBS + Sp).  
  Leave an empty well between each sample on plate 
  (to wash the cytometer).  The easiest way to do 
  this is to use a 12-channel pipet with a tip on 
  every other nozzle to transfer the cells.  
  
  {harvest_table}

""" #
    wash_step = f"""\
- Wash out any ligands:

  - Spin block #{i} at 3500g for 10 min.
  - Discard supernatant.
  - Resuspend each well in 1 mL LB.

""" #
    culture_step = f"""\
- Start the cultures for the next timepoint:

  Transfer 4 μL from the indicated row of each source 
  block into the same row of block #{i+1}.

  {culture_table}

  Incubate at 37°C with shaking at 225 rpm.

""" #
    flow_step = f"""\
- Measure fluorescence via flow cytometry.

""" #

    if i == 0:
        step = title + culture_step
    elif i == 8:
        step = title + harvest_step
    else:
        step = title + harvest_step + wash_step + culture_step

    if i % 3 == 2 or i == 8:
        step += flow_step

    return step


## Prepare media
print(f"""\
- Prepare the following media:

  {media('apo')}

  {media('theo')}

  {media('3mx')}

  {media('theo+3mx')}

""")

## Prepare blocks
print("""\
- Setup the following 24-well blocks:
""")
for i in range(8):
    print(block(i))
print("""\
  Keep each block at 4°C until needed.
""")

## Prepare plates
print(f"""\
- Setup a plate with 250 μL PBS + Sp in each well of 
  the first {longest_timecourse} rows.  Keep at 4°C until needed.

""")

## Start overnights
print("""\
- Start overnight cultures:

  - Make 25 mL LB + Carb + Chlor and transfer 1 mL to 
    each well in rows A-C of a 24-well block.

  - Inoculate the indicated wells with MG1655 
    colonies transformed with the indicated plasmid 
    (within the last two weeks):

    ─────────────────────────────────────
    Wells         Strain
    ─────────────────────────────────────
    A1-C1, A4-C4  on/on (pKBK009)
    A2-C2, A5-C5  off/off (pKBK010)
    A3-C3, A6-C6  rxb 11/rxb 11 (pKBK007)
    ─────────────────────────────────────

  - Incubate at 37°C with shaking at 225 rpm 
    overnight.

""")

## Measure timepoints
for i in range(9):
    print(step(i), end='' if i == 8 else '\n')

