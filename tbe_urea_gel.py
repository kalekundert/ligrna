#!/usr/bin/env python3

"""\
Cast an 8% TBE/urea gel.

Usage:
    tbe_urea_gel.py [<num>]
    
Arguments:
    <num>               [default: 1]
        The number of gels to cast.  Each gel has 15 lanes, which is enough for 
        14 samples and one ladder.
"""

import docopt
import dirty_water
from nonstdlib import plural

args = docopt.docopt(__doc__)
protocol = dirty_water.Protocol()
gel = dirty_water.Reaction("""\
Reagent         Conc  Each Rxn  Master Mix
==============  ====  ========  ==========
urea                    4.2 g 
TBE               5x    2.0 mL
acrylamide/bis   30%   2.67 mL
""")

N = eval(args['<num>']) if args['<num>'] else 1
gel.num_reactions = N
gel.show_totals = False
temed_uL = 10 * N
aps_uL = 10 * N
gels = 'gel' if N == 1 else 'gels'
newline = '\n'

protocol += f"""\
Cast {N} 8% TBE/urea polyacrylamide {gels}.

- Setup the gel cast and make sure it doesn't leak.
  
- Combine the following reagents in a Falcon tube 
  and mix until the urea dissolves (~5 min).

{newline.join('  ' + x for x in str(gel).split(newline))}

- Add {temed_uL} uL TEMED and {aps_uL} μL 0.4 mg/μL APS (freshly 
  prepared), invert once or twice to mix, then 
  immediately pipet into the gel cast.

- Let the {gels} set for 1h.
  
- Either use the {gels} immediately, or wrap {plural(N):/them/it} in a
  wet paper towel and store at 4°C overnight to 
  use the next day."""

protocol += """\
Load and run the {gels}.

- Mix 2 μL of RNA with 2 μL of loading dye.

- Denature at 95°C for 2 min.

- Wash out any urea that's leached into the wells, 
  then quickly load all of the samples.

- Run at 180V for 30 min.
  
- Soak in 3x GelRed for ~15 min to stain."""

if __name__ == '__main__':
    print(protocol)
