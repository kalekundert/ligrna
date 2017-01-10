#!/usr/bin/env python3

import dirty_water

protocol = dirty_water.Protocol()

protocol += """\
Cast an 8% TBE/urea polyacrylamide gel.

- Setup a gel cast and make sure it doesn't leak.
  
- Combine the following reagents in a 15 mL tube 
  and mix until the urea dissolves (~5 min).

  8% TBE/urea polyacrylamide gel
  ──────────────────────────────
  4.2 g urea
  2.0 mL 5x TBE
  2.67 mL 30% acrylamide/bis (29:1)
  water to 10 mL

- Add 10 uL TEMED and 10 μL 0.4 mg/μL APS (freshly 
  prepared), invert once or twice to mix, then 
  immediately pipet into the gel cast.

- Let the gel set for 1h.
  
- Either use the gel immediately, or wrap it in a
  wet paper towel and store at 4°C overnight to 
  use the next day."""

protocol += """\
Load and run the gel.

- Mix 2 μL of RNA with 2 μL of loading dye.

- Denature at 95°C for 2 min.

- Wash out any urea that's leached into the wells, 
  then quickly load all of the samples.

- Run at 180V for 30 min.
  
- Soak in 3x GelRed for ~15 min to stain."""

if __name__ == '__main__':
    print(protocol)
