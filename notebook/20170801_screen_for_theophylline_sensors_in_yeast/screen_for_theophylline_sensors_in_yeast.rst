****************************************
Screen for theophylline sensors in yeast
****************************************

In the process of screening for neomycin and tetracycline sensors in yeast, it 
occurred to me that I should screen for theophylline sensors too.  I think it's 
more likely to work than either tetracycline of neomycin, partly because 
theophylline more commonly used than either antibiotic even in yeast, and 
partly because I already know I can make theophylline sensors in bacteria with 
the same screening strategy.

Methods
=======

Primers
-------
8/1/2017:

I ordered these primers with both 5' phosphate and HPLC/PAGE purification.  The 
extra purification was an extra $400, and I went back and forth on whether it 
was worth it.  I ultimately decided it was.  I really want this screen to work 
as quickly as possible, and avoiding the potential complications of a messy 
library (which was a small problem for the neomycin and tetracyline libraries) 
helps with that.

.. literalinclude:: 20170801_clone_into_sgrna.txt

Transform ux into Top10
-----------------------
8/23/2017:

.. literalinclude:: 20170806_library_prep.txt

The ux transformation worked well the second time I tried it.  I decided to 
repeat the transformation because the first time, most of the ux/3/2 clones 
were missing some nucleotides where the primers came together and I didn't get 
full coverage of either ux/4/3 or ux/5/4.  I remade ux/3/2 (because it had 
mostly the wrong sequence) and ux/5/4 (because I didn't have enough left), but 
just used the original ux/4/3.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL

   theo ux 3,2:
      colonies: 68 8 0 0
      recover: 1000 μL
      conc: 57.0 ng/μL
   theo ux 4,3:
      colonies: x 39 2 1
      recover: 2040 μL
      conc: 151.8 ng/μL
   theo ux 5,4:
      colonies: x x 21 4
      recover: 7314 μL
      conc: 273.0 ng/μL

ux/4/3 and ux/5/4 have mostly the right sequence.  ux/3/2 is missing two base 
pairs from where the primers came together.  Given that I ordered these primers 
with HPLC/PAGE purification --- unless I made an error copying and pasting the 
primer sequence into the order form --- it seems like Elim just sent me bad 
primers.  I'm not going to bother reordering new primers for ux/3/2 though, 
since I didn't really expect to find anything in that library anyways.

:download:`tdh1_theo_ux_5_4.dna`

Transform rhi into Top10
------------------------
8/8/2017:

The `rhi` transformation worked far better than I expected.  It makes me a 
little worried that I diluted the cells wrong, or that I'm miscalculating the 
number of transformants, because I changed the way I diluted the cells for this 
transformation.  Usually with the pAN backbone I don't get any colonies for the 
10⁴ and 10⁵ dilutions, so this time I did one less 10x dilution the try to get 
more spots that I could easily count.  Specifically, I put 180 μL SOC in each 
of 4 tubes, put 20 μL transformed cells in the first one, and then continued 
the serial dilution by transferring 20 μL each time.

It's also possible that the good transformation was due to this being a fresh 
batch of competent cells.  That said, normally I don't find that fresh cells 
are that much more competent than frozen ones.  Another possibility is that 
this prep was just better than my others have been.  If that's the case, it's 
worth noting that I didn't perfectly follow the electrocompetent cell prep 
protocol (because I had some time constraints):

- I abbreviated the final spin (before bringing to 6 mL and aliquoting) to 8 
  min.  The supernatant still looked a little cloudy, but I poured it out 
  anyway.  The pellets were still big, and I didn't think the supernatant 
  would've gotten much less cloudy in the last 2 min.

- After that final spin, I immediately discarded the supernatant, then let the 
  cells sit on ice (in the cold room) for 45 min (while I had another 
  appointment).  Then I added 1 mL 10% glycerol to each tube (4 mL in total), 
  then resuspended and aliquoted the cells.

  I can see how this 45 min rest could've substantially affected two things.  
  First, the cell pellet was much looser when I came to resuspend it, so I 
  didn't have to pipet nearly as aggressively as I usually do.  Perhaps this 
  meant damaging fewer cells.  Second, more 10% glycerol had time to collect in 
  the bottom of the tube, so I ended up with ~7 mL of cells rather than 6 mL.  
  At the time I was worried that this would hurt the transformation efficiency 
  a bit (i.e. less cells, less transformants), but it's possible that it 
  helped, too.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL

   theo rhi 4,4:
      colonies: x x 69 5
      recover: 2032 μL
      conc: 115.8 ng/μL
   theo rhi 4,5:
      colonies: x x 54 10
      recover: 3070 μL
      conc: 100.0 ng/μL
   theo rhi 5,4:
      colonies: x x 85 7
      recover: 3057 μL
      conc: 147.9 ng/μL
   theo rhi 5,5:
      colonies: x x 81 10
      recover: 4089 μL
      conc: 137.1 ng/μL

All the libraries sequenced well:

:download:`tdh1_theo_rhi_5_5.dna`

Transform ux into yBMH139
-------------------------
9/4/2017:

I used 33 μL of plasmid DNA.  At the end of the prep, I also resuspended the 
cells in 2.4 mL water instead of 1 mL and plated 300 μL on each of 8 plates (I 
only had 9 plates, and I used one for the titer).

.. literalinclude:: 20170912_chemicompetent_dueber.txt

Despite scaling the transformation up 2x relative to the rhi transformation 
(see below), I got 2x fewer transformants.  I'm not sure if this means I fucked 
up, or if there are diminishing returns to scaling up (i.e. poor heat shock or 
something).

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3
   :plate: 40 μL

   theo ux:
      colonies: x 15 2
      recover: 2400 μL
      library_size: 1024 + 16384 + 262144

My actual coverage is a little worse than this because I discarded two plates 
due to contamination and cut mold colonies out of three others.

Transform rhi into yBMH139
--------------------------
8/28/2017:

I scaled the protocol 6x.  This was limited by the amount of YPD I had on hand, 
but I don't think I could go too much past 10x without running into shortages 
of other reagents as well.

I only made 5 mL of overnight culture, so I used all of it to inoculate 300 mL 
YPD.  I grew the cells for 5h40 (although they reached OD=1.0 at 5h30):

.. od::

   0h00: 0.0823
   3h59: 0.4213
   5h15: 0.2848 * 3

I linearized 60 μg of DNA (32 μL at ≈2 μg/μL).  I setup the NotI digestion like 
so:

- 32 μL DNA
- 4 μL 10x CutSmart buffer
- 4 μL NotI-HF

I prepared fresh PEG3250 while the cells were growing, and used an ice slurry 
to quickly bring it to 0°C.

I plated the cells on SD-Leu plates.  Previously I'd been using SD-His-Leu, but 
with the healthier BMH139 strain, I'm less worried about losing the fluorescent 
population.

.. literalinclude:: 20170902_chemicompetent_dueber.txt

I didn't get very good coverage, but this is the best transformation I've done 
so far.  I think I would've gotten near full coverage of the ux library.  I 
also don't have the issue with large and small colonies (they're all the same 
size, and look pretty healthy), which makes me feel more comfortable.

The plates themselves aren't quite a lawn, but there are too many colonies to 
count directly.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 23 μL

   theo rhi:
      colonies: x 36+7 6 0
      recover: 1000 μL
      library_size: 65536 + 262144 + 262144 + 1048576

Screen tdh1/ux
--------------
9/12/17:

- Prepare media

  - Mix 30 mL YPD and 1 μL 3.6 mM estradiol
  - Split into two 14 mL portions.
  - To one, add 466.67 μL 72 mM NaOH (YE)
  - To the other, add 466.67 μL 30 mM theophylline + 72 mM NaOH (YET)
    
  I decided to use ligand dissolved in base because it stays dissolved better, 
  and I know it works well because I used it last week for the multiplexing 
  experiment.  It may also be that the plastic tube has fewer nucleation sites.

- Scrape the library off of the plates it was transformed onto and into 50 mL 
  YPD.

- Start the overnight cultures:

  - Library: 24 μL into 12 mL YE/YET
  - Controls: Suspended multiple on/off colonies in 9 μL YPD, then 4 μL into 1 
    mL YE/YET.  I decided to use multiple colonies because the most important 
    thing is for the controls to grow similarly to the library, so their 
    fluorescence values are comparable.  This means getting the starting OD 
    about right.  The plate I'm using was struck from a single colony anyways, 
    so all the colonies should be isogenic.

9/13/17:

- Prepare media as yesterday.

- Start day cultures

  - 200x dilution: 8h is 40x growth, and add an extra factor of 5 because I 
    want to catch the cells in log phase (OD≈2.0).

  - Library: 60 μL into 12 mL YE/YET
  - Controls: 5 μL into 1 mL YE/YET

- Sort the library:

  - The on gate is more sparsely populated.  This is the ux library, which 
    should be on without ligand and off with it (i.e. screening for backwards 
    designs).  That means I want to screen the apo culture.

  - Pellet 5 mL of the library and resuspend it in an equal volume of PBS.  
    Adjust flow rate to 1.0 to get event rate of ≈2500 evt/sec.

  - Gate: 1.0% most on

    - Pretty much to whole on control population
    - 0.6% of the off control population falls in this gate, so I'm not really 
      getting great separation.

  - Sort at 2500 evt/sec for 30 min.  Collect cells in 4 mL YPD.
    
- Grow cells overnight at 30°C with shaking at 225 rpm.  The sorter added a 
  negligible volume to the collection media, so I didn't add any more YPD.

9/14/17:

- Let cells grow all day.  

- Start overnight cultures as on 9/12/17.

   - Library: 48 μL into 12 mL (more than two days ago because I was assuming 
     the scraped cells were OD≈20, while I'm assuming the overnights are 
     OD≈10).
   - Controls: 4 μL into 1 mL.  I picked a new colony for the on cultures, 
     because the overnight didn't grow well.

9/15/17:

- Make media as before.

(I lost my notes for the rest of the day)

Screen tdh1/rhi
---------------
10/26/17:

- Start overnight cultures of the tdh1 controls and the library.

   - Library: Thaw a glycerol stock on ice for 10 min, then inoculate 50 mL of 
     YPD with the whole stock.
   - Controls: For each control, inoculate 1 mL of YPD with a freshly picked 
     colony.

10/27/17:

- Prepare fresh theophylline:

   - 9.6 mg theophylline
   - 1728 μL water
   - Incubate at 50°C until dissolved.

- Prepare media

   - Mix 30 mL YPD and 1 μL 3.6 mM estradiol
   - Split into two 14 mL portions.
   - To one, add 466.67 μL water (YE)
   - To the other, add 466.67 μL 30 mM theophylline (YET)
    
- Start day cultures

   - Library: 60 μL into 12 mL YE/YET
   - Controls: 5 μL into 1 mL YE/YET

- Grow at 30°C for 9h.

- Sort the library:

   - Record the controls and the library.

   - Dilute the library ≈20x to get an ≈1500 evt/sec event rate.

   - Gate: apo culture, 4.5% most off

   - Sort for 1h.  Collect cells in 4 mL YPD.

- Start overnight cultures.

   - Dilute sorted cells into 50 mL YPD and incubate at 30°C.

10/28/17:

- Restart overnight cultures.

   - After 16h (i.e. at 5:00 PM), dilute 1 mL of the library into 50 mL fresh 
     YPD.  The library was at OD=0.4004, so this 50x dilution was approximately 
     designed to get the cells to OD=10 around 9:00 AM tomorrow.

   - Dilute 4 μL of the controls into 1 mL fresh YPD.  I diluted the controls 
     4x more than the library because the cultures looked a little thicker, but 
     I didn't measure their ODs.
     
10/29/17:

- Start day cultures.

   - Prepare 14 mL YE and YET as before.

   - Library: 48 μL into 12 mL YE/YET (this should've been 60 μL but I was 
     looking at the wrong experiment.)

   - Controlssharelatex: 4 μL into 1 mL YE/YET (this should've been 5 μL, but I was 
     looking at the wrong experiment.)

- Grow at 30°C for 9h.

- Sort the library:

   - The cultures were not saturated after 9h, maybe OD=1.

   - Dilute 120 μL of the library into 3 mL PBS to get ≈1000 evt/sec at flow 
     rate "11".

   - Gate: theo culture, 0.4% most on

   - Sort for 30 min.  Collect cells in 4 mL YPD.

- Incubate at 30°C without further dilution (only ≈6000 events were sorted).

Swap spacers
------------
11/15/2017:

I started overnight cultures from glycerol stocks 448 and 452.  I used 25 mL 
YPD and 1 mL of each glycerol stock.

In the morning, I was concerned that the cultures had become contaminated 
because they smelled very sharp.  I decided to plate 10⁴ dilutions of both 
cultures on YPD plates to see if I could detect any bacterial contamination.  
However, I also noticed that the cultures settled within a few hours, which 
bacterial cultures wouldn't do.  Perhaps the sharp smell just indicates that 
the yeast were overgrown (very possible given how much glycerol stock I used).

I decided to do 35 cycles of PCR instead of 25, since I think the problems I 
had last time may have been attributable to just not having enough insert.

I decided to Nanodrop all the components before setting up the Golden Gate 
reaction (in the spirit of troubleshooting).  I found that the colony PCR'd 
inserts were ≈80 ng/μL --- pretty good --- but the linearized backbone was only 
≈10 ng/μL --- barely above the noise since there was a relatively big 
guanidinium peak.  There should be a lot more than that, since I started with 
800 ng/μL DNA and diluted it only 5x for the restriction digest.  I'm going to 
repeat the digest tomorrow.

.. update:: Nov 17, 2017

   I repeated the digest and got 160 ng/μL linearized and gel-purified 
   backbone.  That's definitely good enough to use, but I'm not really happy 
   with the yield because it still means I need to add a lot of backbone to get 
   the same number of molecules as the insert.  I'm weighing skipping the gel 
   purification step next time...

I decided (somewhat on a whim) to use 4 μL of desalted DNA for the 
transformation instead of my usual 2 μL.

.. literalinclude:: 20171115_swap_spacer.txt

The PCR reaction wasn't particularly clean, and I'm wondering what to do about 
that.  The options that I can see are: ignore it, gel purify it, run a Tm 
gradient, or order new primers.  I don't want to gel purify it, because I'm 
worried as it is about having enough insert, and I'll probably lose a lot 
trying to do a gel purification.  It would probably be worth doing a Tm 
gradient to see if I can solve the problem easily.  But in the meantime I don't 
think any harm will come from ignoring it.  I should easily be able to cover 
these libraries even with some weird fusion products, and the expected product 
is the major product anyways.

Another thing that's worth noting is that I seemed to get much more product 
this time than last time.  (I don't think the product was cleaner last time, 
but it's hard to tell because the bands are fainter and closer together.)  This 
is probably directly attributable to doing 35 cycles rather than 25, since I 
didn't change anything else about the colony PCR procedure.

.. figure:: 20171115_ux_rhi_colony_pcr.png
   :width: 400px

   Colony PCR products.  2% agarose/TAE/GelRed gel run at 100V for 1h.  From 
   left to right: GeneRuler 100 bp Plus ladder, negative control PCR (−yeast), 
   ux library, rhi library.  The expected product sizes are 197 bp for ux and 
   194 bp for rhi.

I setup a gradient using the same primers and zymolase reactions from this 
morning.  It's possible that sitting in lysed cells at room temperature all day 
isn't good for the genomic template DNA, but I guess we'll see.

It doesn't appear that Ta optimization is sufficient to get rid of the minor 
products.  I'll probably continue ignoring the minor products unless they end 
up causing problems (i.e. everything I isolate is a weird fusion) down the 
road.  I don't know what happened to the second lane from the right...

.. figure:: 20171115_colony_pcr_tm_gradient.png
   :width: 400px

   Annealing temperature gradient.  2% agarose/TAE/GelRed get run at 100V for 
   1h.  From left to right: GeneRuler 100 bp Plus ladder, 68°C, ..., 52°C.

11/17/17:

I lost the sort reports for the first ux screens, so I don't really know how 
many library members are left, but I don't think if was more than a few 
thousand.  I entered 10,000 below as a conservative guess.  With nearly 10⁷ 
transformants, I definitely have complete coverage.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL
   :recover: 1000 μL

   theo tdh2 ux:
      colonies: x x 133 16
      library_size: 10000
   theo tdh2 rhi:
      colonies: x x 159 27
      library_size: 10000

Retransform into yBMH139
------------------------
11/21/17:

I decided to to try a new transformation protocol: Gietz2007_.  My hope was to 
get more transformants.  These libraries are small enough that I don't need 
better efficiency for them, and really I was viewing this as a practice run for 
the rbi library.  Differences in the protocols aside, the Gietz2007_ protocol 
is also less ambiguous than the Dueber protocol, so I thought I might be able 
to get more transformants simply by doing things more correctly.

I made 500 mL 2x YPAD as follows:

- 50 g YPD powder (10 g yeast extract, 20 g peptone, 20 g dextrose)
- 40 mg adenine

.. note:: 

   I tried making a 100x stock solution of adenine, but found that it was too 
   insoluble for that.  I probably could've made a 10x solution, but it seemed 
   like too much effort, so I just weighed out 40 mg.

I grew the overnight cultures in 50 mL YPD (not YPAD).  The culture wasn't 
dense enough when I got to lab, so I let it grow for another 2h before starting 
the protocol.  By then, the OD was 2.479 (10 × 0.2479).  I should've used 25.21 
mL for each of the two cultures I wanted to start, but I only used 24 mL 
because I only had 50 mL of overnight.

I measured the OD of the culture even though the protocol just says to grow for 
2 doublings, which I know is 3h for this strain.  I guess it's a good thing I 
did, because the yeast hadn't quite quadrupled by 3h13.  I ended up growing the 
cultures for 4h04 (the protocol suggested that it wouldn't be a problem to 
overgrow by even a few hours):

.. od::
   :dilution: 10x

   A (0h00): 0.0454
   B (0h00): 0.0478
   A (3h13): 0.1739
   B (3h13): 0.1781
   A (4h04): 0.2303
   B (4h04): 0.2452

At the end of the protocol, I suspended the cells in 12 mL water, but I only 
plated 1.2 mL.  I did this because I was planning to plate the rbi library on 
30 plates (which would require resuspending in 12 mL for 400 μL/plate), and I 
wanted to get the same cell density so I could compare the transformations.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL
   :recover: 1200 μL

   tdh2/ux:
      colonies: 14 2 0 0
      library_size: 10000
   tdh2/rhi:
      colonies: 79 9 0 0
      library_size: 10000

This was an awful transformation, but it would've been fine if I'd actually 
plated all the cells.  In any case, I probably still got reasonable coverage of 
the remaining library members.  Also, none of my plates have any contamination, 
so it seems that my sterile technique was the problem, and that wiping down my 
bench and keeping the lids on the culture dishes as much as possible was the 
key.

Screen tdh2/ux
--------------
11/28/2017:

- Resuspend library and start overnight cultures.

   - Add 5 mL YPD to each of the 3 library plates, and use a cell scraper to 
     resuspend the cells.  Pipet the resuspended cells off the plates and into 
     a 50 mL falcon tube.  I ended up with about 10 mL.

   - Library overnights: 12 mL YPD, 48 μL resuspended cells.  These volumes 
     were pretty arbitrary.  I was loosely copying from the first screen in 
     this experiment.  I decided to add twice as many cells because the first 
     screen already had estradiol in the overnights, so I probably timed it to 
     be getting close to saturation after 12-16h.  This time I want the 
     overnight to be completely saturated --- and the faster the better, 
     because it means less bias due to differential growth --- so I added twice 
     as many cells.  The cells are probably more concentrated too, because I 
     didn't dilute to 50 mL YPD.

   - Control overnights: 1 mL YPD, colony picked from very old plate.  I wanted 
     to use a glycerol stock, but apparently I never made any.  I'll make some 
     tomorrow so this won't be a problem in the future.

   - Make glycerol stocks.  I figure it's better to make stock now --- before 
     there are any biases due to growth --- than later.

11/29/2017:

- Prepare fresh theophylline

   - 4.9 mg theophylline
   - 882 μL water
   - Incubate at 50°C until dissolved.

- Prepare media

   - Mix 30 mL YPD and 1 μL 3.6 mM estradiol
   - Split into two 14 mL portions.
   - To one, add 466.67 μL water (YE)
   - To the other, add 466.67 μL 30 mM theophylline (YET)

- Start day cultures

   - Library: 10 μL into 2 mL YE/YET
   - Controls: 10 μL into 2 mL YE/YET

   - I realized that I didn't have enough media to do the usual 12 mL, because 
     I'm doing ux and rhi in parallel.  I thought about just doing 6 mL, but I 
     decided that the libraries are now small enough to grow in just 2 mL, and 
     that would let me use culture tubes.

- Grow at 30°C for 9h.

- Sort the library:

   - Record the controls and the library.

   - Dilute 73 μL into 3 mL PBS to get ≈1000 evt/sec.

   - Gate: apo culture, 5.4% most on

   - Sort for 5m.  Collect cells in 1 mL YPD.

- Grow collected cells overnight.

12/1/2017:

- Prepare theophylline and media exactly as before.

- Make 1 mL day cultures with 5 μL overnight.

- Grow at 30°C for 9h.

- I didn't sort because there was clearly no response to ligand.

Screen tdh2/rhi
---------------
11/28/2017:

Same protocol as for screening tdh2/ux.

First screen: apo culture, 2.0% most off


Results
=======
I was not able to isolate theophylline-sensitive clones for either library.  At 
no step was there even a hint of ligand-sensitivity:

.. figure:: 20170913_screen_theo_ux.svg

   Flow cytometry traces of the ux library.

.. figure:: 20171027_screen_theo_rhi.svg
   
   Flow cytometry traces of the rhi library.

It's worth spending some time thinking about why these selections may not have 
been successful.

- Both libraries were very small, only about 10⁵.  In contrast, my bacterial 
  libraries were closer to 10⁷, I think.  I wonder if I would've gotten better 
  transformation efficiencies if I'd used plasmids instead of trying to 
  integrate everything.

- My libraries may have been too "bacteria-oriented".  By this I mean that I 
  had to really reduce my library size to account for the poor transformation 
  efficiency in yeast, and one of the ways I did this was by fixing positions 
  that were relatively conserved in the bacterial screens.  But I already knew 
  that the particular sequences I identified in bacteria didn't work in yeast, 
  so maybe it wasn't a good idea to bias my libraries towards those constructs.  
  (Although I'm not sure how else I could've shrunk the libraries...)  But this 
  could explain why I didn't have success with the ux library despite getting 
  28% coverage (which isn't good, but it's probably good enough to have fully 
  covered base-pairing space).

- I wonder if the ribozyme inserted before the sgRNA could've messed with 
  things.  Ben and Andrew thought this was for the best, and clearly it wasn't 
  a problem for the controls, but I wonder if it could've interfered with the 
  aptamer somehow.  For example, maybe when the RNA was folding, the aptamer 
  could've spent time interacting with the partially folded ribozyme when it 
  otherwise would've been interacting with theophylline.  That rationale is 
  kind-of a stretch, but I do think this would be worth reading more about if I 
  were to do these screen again.

- In Ben Oakes' methods paper on screening Cas9 libraries, he had a different 
  method for yeast.  It was survival based, rather than FACS based.  I wonder 
  if I would've had more luck with that method.

Troubleshooting
===============

Transform ux into Top10 --- Aug 5, 2017
---------------------------------------
I didn't have enough competent cells to transform both libraries at once, so I 
transformed the ux library on the first day, then made fresh competent cells, 
then transformed the rhi library on a second day.

The first Top10 transformation I tried didn't quite reach 100% coverage.  I'm 
going to miraprep the cultures anyways, and repeat the transformations if the 
opportunity arises.

.. note::

   The opportunity did arise, and I got better results the second time.  See 
   `Methods`_ for more info.

.. electrotransformation::
   :plate: 40 μL
   
   theo ux 3,2:
      colonies: 12+18 1 0 0
      recover: 1020 μL
   theo ux 4,3:
      colonies: 17+14 1+2 0 0
      recover: 1020 μL
   theo ux 5,4:
      colonies: 31+35 2+2 1 0
      recover: 3170 μL

This is despite the PCR working very well:

.. figure:: 20170804_clone_theo_ux_rhi.svg
   :align: center

I made new competent cells for the `rhi` transformations, and they worked much 
better (see `Methods`_).

Transform ux into yBM139 -- Aug 24, 2017
----------------------------------------
I used 4.4 μL of 3608.7 ng/μL DNA, for a total of 16 μg.  I also shortened all 
the spin steps to 2 min.  I figured that if the pellets were looser and I could 
resuspend them more gently, more cells might survive.  I plated the cells on 9 
81 cm² plates:

.. literalinclude:: 20170825_yeast_library_prep.txt

The library was sparse enough that I could count individual colonies.  I 
counted 83 colonies in one representative-looking 1.35 cm² area.  With a total 
plate area of 9 × 81 cm² = 729 cm², that corresponds to 44,820 colonies, about 
half of what I counted with the titer.

.. electrotransformation::
   :dilutions: 5 ^ 1 2 3
   :plate: 20 μL

   theo ux:
      colonies: 17 9 2
      recover: 20800 μL
      library_size: 1024 + 16384 + 262144

There were also maybe 3x more small colonies that I didn't count for either 
method.  I felt that these colonies were so small relative to the larger ones 
that they would contribute a negligible number of cells to the library, not 
even considering that they may continue to grow slower even in liquid media.

The coverage of the transformation isn't good, but I think it's good enough.  
Most base-paired variants of rxb 11,1 work to some degree, so even missing 2 of 
every 3 library members, I should be able to find working designs.

Theo ux contaminated with bacteria --- Aug 28, 2017
---------------------------------------------------
This protocol largely follows :expt:`20170401_screen_for_neomycin_sensors`:

- Prepare media

  - Mix 30 mL YPD and 1 μL 3.6 mM estradiol
  - Split into two 14 mL portions.
  - To one, add 466.67 μL milliQ water (YE)
  - To the other, add 466.67 μL 30 mM theophylline (YET)

- Scrape the theo ux library off its plates and into 50 mL YPD.

  I discarded one plate due to the presence of mold.

- Make a glycerol stock of the library.

- Start the library growing in YE and YET (7:00 PM).

  I assumed the resuspended cells were at OD=20 as they were with the neomycin 
  library, and inoculated 12 mL Ye and YET with 24 μL of the resuspended 
  library.

  For the controls, I started 1 mL cultures from freshly picked colonies.

- Measure the controls in the morning (11:00 AM).

  I had to grow BMH127 for 24h the get the best signal, but BMH139 is much 
  healthier and probably doesn't need as much time.  So I measured the 
  fluorescence in the morning to see what the controls look like after just 16h 
  growth.

  I diluted 10 μL cells into 250 μL PBS for flow cytometry.

- Subculture the library into YE and YET again (12:00 noon).

  I was worried that 24h would be too long, so I wanted to try starting new 
  cultures 7h before sorting.  7h is 4.67 doublings, which is a 25x increase in 
  population.  I arbitrarily decided that OD=2.0 would be a good ending point, 
  so I diluted my cultures to OD=0.08.  I assumed that my overnight cultures 
  were at OD=10.0, so I used 8 μL cells for my 1 mL controls and 100 μL for my 
  12.5 mL libraries.

- Run controls (subcultured and not) on the FACSAria II (7:45 PM).

  The 24h controls had a fold change of 16.7x, and the off control was 
  noticeably bimodal.

  The 7h controls had a fold change of 26.7x, and both were unimodal.  0.3% of 
  the off control fell in the on gate (compared to 0.0% for the 24h off 
  control), so there were slightly more stragglers in the shorter culture.

  I decided to use the 7h cultures for the screen.

- Transfer the library to PBS:
  
  - Pellet 5 mL of the library.
  - Discard supernatant and resuspend in 5 mL PBS.

- Pick sort speed and time:
  
  I want really good coverage, because my transformation had colonies of 
  different sizes, and I want the small colonies to be fully represented if 
  possible.  I decided to go for 25x (assuming the whole library was 
  transformed -- it's hard to say for sure how many transformants I have 
  because I couldn't really count the small colonies): 30 min at 9000 evt/sec.

- Pick gates:

  4.1% most on: This gate was mostly coincident with the on control population.  
  There was 0.3% of the off control in the gate, but I couldn't have improved 
  that much by simply making the gate smaller.

- Sort the library

  I got the event rate to 10,000 evt/sec by adjusting the flow rate to "5", 
  then sorted for 30 min and collected the cells in 4 mL YPD.  I ultimately 
  collected about 2 mL of volume.

- Dilute the library to 25 mL, subculture 20 μL of each control into 1 mL fresh 
  YPD, and grow for 24h at 30°C with shaking at 225 rpm.

- Subculture the overnight cultures into YE/YET (8:30 PM).

  - Make media as before.

  - Dilute 250x (4 μL for the controls, 48 μL for the library)

- Subculture the library into fresh media.

  This time there were 8h30 before the sort, so I diluted the cells 50x instead 
  of 25x.  This should give me the same OD in the end.  Prepare YE and YET as 
  before.

  - controls: 1 mL media, 4 μL overnight culture
  - library: 12 mL media, 48 μL overnight culture

- Sort the library

  My cultures seem to have been contaminated with bacteria:

  - There were no events in the FSC vs. SSC gate that characterizes live yeast, 
    but there was a large population with smaller FSC  values and higher SSC 
    ones.  Smaller size and higher internal complexity is consistent with 
    bacteria, I think.

  - I tried running the overnight culture as well (even though it had just been 
    sitting on my bench for 8h), and saw the same thing.

  - Both the overnight and the day cultures smelled bright and sharp.  Not like 
    S. cerevisiae or E. coli,really.

  - The day cultures were clearly more dense than OD=2.0, so it's fair to say 
    that the contamination can grow faster than yeast.

Theo rhi didn't grow after screen --- Sep 4, 2017
-------------------------------------------------
- Prepare media

  - Mix 30 mL YPD and 1 μL 3.6 mM estradiol
  - Split into two 14 mL portions.
  - To one, add 466.67 μL milliQ water (YE)
  - To the other, add 466.67 μL 30 mM theophylline (YET)

- Resuspend library in YPD.

  3 of 9 plates had mold or red yeast.  I wonder if this is due to how I dry 
  out the plates (i.e. open and maybe not close enough to a flame).

- Start the overnight cultures:

  - Library: 24 μL into 12 mL YE/YET.
  - Controls: Resuspend a single colony in 18 μL YPD, then 8 μL into 1 mL 
    YE/YET.

- Grow overnight at 30°C with shaking at 225 rpm.

- Start the day cultures:

  - Prepare YE/YET as above.
  - Library: 48 μL (to get OD≈2.0 after 8h30 growth) into 24 mL YE/YET
  - Controls: 4 μL would be the same dilution, but I used more because the 
    overnights look thin:

    - on: 8 μL into 1 mL YE/YET
    - off: 16 μL into 1 mL YE/YET

- Grow for 8h30 at 30°C with shaking at 225 rpm.

- Sort the library

  - The off controls were very smeary.  I'm attributing this to them being in a 
    different phase of the cell cycle because I diluted them too much.

  - Pellet 2 mL theo rhi and resuspend in 4 mL PBS.  Event rate: 5000 evt/sec 
    at flow rate 1.0.

  - Gate: 5.0% most on (≈⅔ of on control population)

  - Sort the theo condition for 30 min at 5000 evt/sec to get about 20x 
    coverage.  Collect cells in 4 mL YPD.  The sorter produced about 1 mL of 
    fluid, so the final volume was 5 mL.

- Grow cells overnight at 30°C.

  The cells did not grow.  This is the second time this has happened to me, and 
  in both cases I tried to grow cells in YPD with ≈25% or more PBS from the 
  sorter.  I suspect that the problem is due to the charge the sorter puts on 
  the droplets to sort them, because the conventional wisdom is that yeast grow 
  fine in YPD that been diluted even 50%.  In any case, it seems adding 50 mL 
  YPD is a way to solve this problem, so I just have to be more consistent 
  about doing that.

Poor BsmBI cleavage --- Oct 16--17, 2017
----------------------------------------
I decided to linearize and gel purify pKBK017 before doing the Golden Gate 
assembly to create the tdh2/ux library.  My concern was that it I skipped this 
step, a significant fraction of my library might end up without an insert.

1. Setup the BsmBI digest:

   - 6 μL water
   - 2 μL vector DNA (tdh2 BsmBI)
   - 1 μL 10x NEBuffer 3.1
   - i μL BsmBI

2. Incubate at 55°C for 40 min, then at 80°C for 20 min.

3. Add 2 μL 6x loading dye to the reaction, then load all of it into a 1% 
   agarose/TAE/GelRed gel.  Run at 100V for 1h.

The expected product is 5.7 kb (the topmost bright ladder band is 6kb).  Some 
of the DNA appears to be linearized, but not much.

.. figure:: 20171016_linearize_tdh2_bmsbi.png

   Oct 16, 2017

I attributed this failure to bad enzyme.  There were two tubes of BsmBI in the 
freezer, and I used the one that was almost empty in the interest of finishing 
it.  I repeated this experiment with exactly the same setup the next day, but 
with the fuller tube.  I also ran some of the uncleaved plasmid on the gel, to 
be more sure which band was due to cleavage.

I should've run this gel longer; it's hard to tell exactly which band is due to 
the restriction enzyme.  Regardless, it's clear that the old tube wasn't the 
(only) problem.

.. figure::  20171017_linearize_tdh2_bmsbi.png

   Oct 17, 2017

I again setup the exact same reaction as before, but this time I incubated it 
at 55°C overnight.  This reaction also didn't work.

Ugh, I looked back at my plasmid map and realized that I cloned in *BsaI* 
sites, not BsmBI ones.  I repeated the reaction with BsaI and it worked 
perfectly.

Swap ux spacer --- Sep 16, 2017
-------------------------------
The protocols for yeast colony PCR that I can find online all assume that 
you're actually starting from a colony.  I wanted to use about the same numbers 
of cells as those protocols, even though I'm starting from liquid culture, so I 
looked up some bio-numbers:

- Number of cells in a yeast colony: ≈1e6
- Number of cells in 1 mL of OD=1 culture: ≈3e7

Assuming my overnight cultures are at OD=10, that means I would need 3.3 μL to 
get about a colony-worth of cells.

- Pellet the overnight culture and resuspend it in an equal volume of PBS.  (I 
  don't really think this step was necessary; I just decided to do it because 
  it seemed very proper.)

- Setup the zymolase reaction:
   
   - 49.4 μL water
   - 3.3 μL yeast
   - 0.6 μL 5U/μL zymolase (50 U/mL final)

- Incubate at 37°C for 30 min, then denature at 95°C for 10 min.

- Setup a 50 μL PCR reaction:

   - 15 μL water
   - 5 μL primer mix
   - 5 μL zymolase reaction
   - 25 μL 2x Q5 master mix

- Run the PCR reaction:

   - 22 cycles
   - Extension time: 12s
   - Annealing temperature: 60°C

.. figure:: 20171016_tdh1_uh_colony_pcr.png
   :width: 400px

   GeneRuler 1 kb ladder.  The last ladder band is 250 bp, while the expected 
   product is 147 bp.

Oct 20, 2017:

- Setup the restriction digest of the destination vector:

   - 6 μL water
   - 2 μL ≈800 ng/μL pKBK017 
   - 1 μL 10x CutSmart buffer
   - 1 μL BsaI-HF

- Incubate at 37°C for 30 min, then at 65°C for 20 min.

- Gel purify the entire reaction (even though the cleavage efficiency was very 
  high).

- Setup a Golden gate reaction:

   - 5.0 μL water
   - 1.0 μL pKBK017 (linearized and gel purified)
   - 2.0 μL ux insert (amplified from yeast genome)
   - 1.0 μL 10x T4 ligase buffer
   - 1.0 μL T4 ligase
   - 1.0 μL BsaI-HF

- Run the following thermocycler protocol:

   - 42°C for 5 min
   - 16°C for 5 min
   - Repeat 30 times

Nov 1, 2017:

Electrotransform...

Nov 2, 2017:

I lost the sort reports for the first ux screens, so I don't really know how 
many library members are left, but I don't think if was more than a few 
thousand.  I entered 10,000 below as a conservative guess.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL
   :recover: 1000 μL

   theo/tdh2/ux:
      colonies: 68 8 2 0
      library_size: 10000
      conc: 2.4 ng/μL

Nov 3, 2017:

Sequencing failed.  I'm not sure what I ended up with, but it doesn't seem to 
have the expected plasmid backbone...

Swap rhi spacer --- Oct 31, 2017
--------------------------------
Protocol identical to "Swap ux spacer" above.

The electrotransformation failed for this construct: I got no colonies.


References
==========
.. [Gietz2007] Gietz, R. Daniel, and Robert H. Schiestl. “Large-Scale 
   High-Efficiency Yeast Transformation Using the LiAc/SS Carrier DNA/PEG 
   Method.” Nature Protocols 2, no. 1 (January 2007): 38–41. 
   https://doi.org/10.1038/nprot.2007.15.


