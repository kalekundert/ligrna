***************************
Screen for neomycin sensors
***************************

Neomycin is an aminoglycoside antibiotic for which several aptamers have been 
developed.  I'm interested in creating sgRNAs that are activated and inhibited 
by neomycin.  In order to do this, I need to move my system to yeast, since 
neomycin is (obviously) toxic to bacteria.

Library design
==============

Picking an aptamer
------------------
There are several RNA motifs that bind neomycin, but to my knowledge only N1 
and N2 from Weigand08_ have been used to regulate gene expression:

.. figure:: weigand08_fig_6.png

    A-site is the neomycin binding site in the bacterial ribosome.  Neo5 and 
    Neo61 came from a SELEX screen.  The GGG UUU motif exhibited by Neo61 was 
    present in most of the aptamers identified in that screen; Neo5 was an 
    outlier.  N1 and N2 came from an in vivo screen.  Only N1 and N2 are 
    capable of regulating GFP expression in vivo.

It's interesting to note how similar all these binding motifs are.  Despite 
that similarity, only N1 and N2 regulate GFP expression in vivo.  Even A(N1), 
which is identical to N1 except for having the A-site bulge, doesn't respond to 
neomycin.

Neomycin is believed to bind in the pocket created by the bulge (or by the GGG 
UUU motif, which is known to make the helix wider than usual).  The hairpin is 
then believed to fold over and hold the neomycin in place.  I'm not sure if 
neomycin binding actually induces a conformational change in the aptamer (like 
it does with theophylline), but the fact that N1 and N2 can regulate gene 
expression makes me think they could probably regulate sgRNAs too.

I'm going to use the N1 aptamer for my libraries, because it consistently 
performed slightly better than N2.  Note that Weigand08_ optimized their 
sensors (from 2.5x to 7.5x) by rationally changing the stem length.  I'm 
planning to randomize the stem instead, much like I did for the theophylline 
aptamer.

Designing a "backward" library
------------------------------
The only question for the backward library is how long to make the stem.  I can 
transform about 4×10⁵ cells, which corresponds to randomizing 9.3 positions.  I 
will keep U59 in place, since it's essential to the mechanism I want to evolve.  
Additionally, ``w11 1`` showed that the bottom base pair in the nexus is 
important, so I will keep that in place too.  Since on top of that the aptamer 
ends in its own GC base pair, I would only need to randomize 5 positions to 
make a library that includes ``rxb 11,1``.  While I'm at it, I might as well 
try making the stem 1 bp shorter and 1 bp longer.

I will call this library ``ux``.  James already made a ``ux`` library that does 
just what I describe above, except it also randomizes the base pair on the 
bottom of the nexus.  Since we now understand that to be suboptimal, I will add 
an optional 'g' argument to keep that base pair unrandomized.  So the final 
names for these libraries will be:

- ``neo ux 3,2,g``
- ``neo ux 4,3,g``
- ``neo ux 5,4,g``

Designing a "forward" library
-----------------------------
The first question is whether to randomize the communication module or the 
nexus.  On one hand, my hypothesis is that ``mhf 30`` works by forming a stem 
between the nexus and the 5' side of the aptamer (in the apo state).  Since the 
neomycin aptamer has a different sequence than the theophylline aptamer, that 
suggests I should randomize the nexus.

On the other hand, I can't assume that the communication module I evolved for 
the theophylline will work for neomycin.  Weigand08_ showed that the length and 
strength of that stem is important.  It's also worth noting that ``gfp rhf 6`` 
worked well, even if it was spacer-specific, so it's demonstrably not necessary 
to randomize the nexus (although ``rhf 6`` probably depended on parts of the 
sgRNA base-pairing with parts of the aptamer).

All things considered, I think randomizing the communication module is the best 
course of action.  I want to randomize at least 4 base pairs, and I think it's 
worth trying 5 as well.  

I won't randomize any part of the ruler.  Even though I did that for the ``theo 
rh`` libraries, I don't think it helped.  First, Cas9 doesn't seem to care too 
much about the specific ruler sequence.  Briner14_ only tested two sgRNAs with 
ruler mutations, but both were pretty functional (86% and 67% cleavage).  
Second, the ruler mutations in ``rhf 6`` are not involved in the mechanism 
predicted by ``RNAfold``.  Especially since I'm already pushing the size of 
this library by randomizing 10 positions in the communication module, I really 
can't justify randomizing the ruler.

The ``rh`` algorithm is too far from what I want to use directly, but I still 
think this library falls in the ``r`` family since it's just randomizing the 
communication module, so I'll call the new library ``rhi``.  I think ``i`` is a 
good letter to indicate a variant, because it's narrow and it's followed 
naturally by ``j`` and ``k``, if I ever need to go that far.  The final names 
for this library will be:

- ``neo rhi 4``
- ``neo rhi 5``


Troubleshooting
===============

Top10 transformation
--------------------
Despite these libraries being so much smaller than the ones I've worked with in 
the past, I was having a lot of trouble transforming them into yeast.  I tried 
making fresh competent cells, I tried (unsuccessfully) optimizing the ligation 
reaction once I realized that it looked like not all the DNA was being ligated, 
I tried ordering fresh primers, and I tried incubating the competent cells at 
different temperatures (4°C, 25°C, and 37°C) before electroporating them (I 
found a paper suggesting that this would improve transformation efficiency).

None of that helped (and the cells were markedly less competent at 25°C and 
37°C than at 4°C).  Ultimately, there were two issues:

1. I was calling the ``count_transformants.py`` script wrong, in a way that 
   undercounted by number of transformants by a factor of 10.  (At some point I 
   added the library name as a first argument, but I didn't use that argument 
   for anything and so I just forgot about it.  Then when I called the script 
   without that argument, the first colony count was being interpreted as the 
   library name rather than a count and all the other colony counts were 
   basically shifted over by a factor of 10).

2. The pAN plasmid just cannot be transformed as efficiently as the pBLO 
   plasmid.  I confirmed this be preparing fresh libraries with both backbones 
   (I used the same primers for PCR) and transforming both at the same time.  
   The pBLO library gave me 3.50×10⁷ transformants (which is what I'm used to) 
   and the pAN library gave me 3.47×10⁶ transformants (consistent with all the 
   transformations I'd done with that backbone).

   I can think of two reasons why this might be.  First, pAN is 5.8 kb while 
   pBLO is 2.5 kb.  Longer DNA is said to transform less efficiently (although 
   the papers that say that are usually referring to 50-100 kb plasmids).  
   Maybe this is somehow due to the physics of DNA getting into the cell after 
   electroporation, in which case there's nothing I can do, because pAN is 
   already as small as it can get.  The concentration of the DNA may have also 
   played a role.  Both plasmids were similarly concentrated as measured by the 
   Nanodrop (213.2 ng/μL for pBLO and 136.6 ng/μL for pAN), but since pBLO is 
   about half the size it was ultimately about 3.6x more concentrated in a 
   molar sense (although that cannot fully account for the 10x increase in 
   transformants).

   Second, the two backbones have different resistance markers.  pAN has KanR 
   and pBLO has AmpR.  It's possible that Kan is just more selective, or that I 
   need to recover the cells for longer with Kan (I'm doing an hour right now), 
   or that the Kan plates have too much antibiotic.  I'm dubious about all 
   these things, but I can't be sure that they're unimportant without switching 
   the resistance to AmpR (which I won't do, even though I'd like to).

BMH127 transformation
---------------------
.. literalinclude:: 20170726_yeast_library_prep.txt

I'm worried about this library.  After the transformation, I grew the 
transformed cells in 950 mL SD-LH.  My goal was for the cells that were 
successfully transformed to grow enough to vastly outnumber the cells that 
weren't transformed, so that I would still have mostly library members when I 
subcultured the library into YPD for the actual screen.  I used so much SD-LH 
(950 mL) because the competent cells were prepared from 400 mL of culture at 
OD≈1.6.  I didn't want my culture to start off saturated, because then it 
wouldn't have any room to grow.  (Now that I've written it out, I don't buy 
that argument.  Even if a culture is OD≈10, if most of those cells can't 
divide, there will still be plenty of nutrients for the one that can.)

The next day, the SD-LH culture was very thin.  I didn't measure ODs, but it 
didn't really look like it have grown at all.  (Again, perhaps this was because 
I had a relatively small population of alive cells, and they just didn't have 
time to saturate the culture.  Plus, I don't even know what saturated is in 
SD-LH.)  But I'm worried that if cells didn't grow very much, my library may 
still dominated by cells that don't have an sgRNA.

First screen --- July 26, 2017
------------------------------
1. Prepare media with and without neomycin:

   - 200 mL YPD
   - 6.67 μL 3.6 mM estradiol
   - split into two 100 mL portions
   - to one, add 363.5 μL neomycin
   - to the other, add 363.5 μL water

   The decision to use 100 mL of media was arbitrary.

2. Inoculate the apo and holo media with the controls and transformed library.

   As I established in :expt:`20170510_run_tdh1_controls`, I want to dilute the 
   overnight 250x into fresh media and grow it for 24h at 30°C.  A 250x 
   dilution into 100 mL is 400 μL, so I will use 400 μL overnight culture.

   - 1 mL apo tdh1 on
   - 1 mL neo tdh1 on
   - 1 mL apo tdh1 off
   - 1 mL neo tdh1 off
   - 98 mL apo tdh1 ux/rhi
   - 98 mL neo tdh1 ux/rhi

   .. update:: Jul 28, 2017

      In retrospect, I think I should've subcultured more than 400 μL, maybe a 
      lot more.  The calculation from :expt:`20170510_run_tdh1_controls` 
      assumes that the overnight culture is saturated, but in this case it 
      wasn't even close.  I'm worried that I subcultured so few cells that I 
      didn't get good coverage of the library, even if the transformation 
      worked well.
      
3. Incubate at 30°C with shaking at 225 rpm for 22h.

   .. od::
      
      YE: 0.0833
      YEN: 0.1274

   The library cultures were not saturated after 24h (the control cultures 
   were).  I think this is a direct consequence of the overnight cultures being 
   thinner than expected (and me not subculturing more of them to make up for 
   it).

4. Transfer the libraries to PBS:

   Due to my concerns about the library possibly being dominated by cells 
   without an SGRNA (see the section on the yeast transformation), I wanted to 
   sort as many cells as possible.  In other words, if maybe 99% of cells don't 
   have an sgRNA, I need to screen 100x more cells to still see the whole 
   library.
   
   When sorting "on" cells in yeast, I can sort as fast as possible (20,000 
   evt/sec) without any significant decrease in purity.  However, sorting at 
   this speed requires the cells to be at OD≈2.  That meant concentrating the 
   cells.

   I probably wouldn't have done this if my cells had been more concentrated, 
   but in retrospect it felt more controlled to remove most of the YPD from the 
   samples I'd load on the cytometer.  So maybe I'll keep this wash step even 
   with more concentrated cells.
   
   - Pour 50 mL of each library (out of 98 mL total) into a falcon tube.

   - Centrifuge at 3500g for 5 min at 4°C.

   - Resuspend the pellet in 10 mL PBS.

   At the same time, dilute 10 μL of each control into 1 mL PBS.

5. Record populations for the controls and the libraries, then draw gates for 
   the screens.

   I used the same gate for both screens, and that gate encompassed the 3.9% 
   most on cells.

   After seeing the event rate for the libraries, I decided to concentrate them 
   further to 3 mL.  This gave event rates pretty close to 20,000 evt/sec.

6. Sort each library for about 30 min.  Collect cells in 15 mL culture tubes 
   with 3 mL YPD.  I collected about 2 mL of cells, so I ended up with about 5 
   mL of culture.

7. Incubate the collected cells at 30°C for 24h.

I actually left the cells in the incubator for 4 days, and nothing ever grew.  
This was shocking to me.  I know that about half the cells survive sorting, 
because I plated cells in :expt:`20170720_optimize_sorting_s_cerevisiae`.  The 
only thing I can think is that the large amount of charged PBS (from the 
sorter) killed the cells, or somehow stopped them from growing.


Methods
=======

Ordering primers
----------------
Below are the specific primer sequences I ordered.  I ordered the 5'-phosphate 
modification, but not any special purification, because I think these are short 
enough to not need it.

.. literalinclude:: primers.txt

BMH127 transformation
Transform ux into yBMH127
-------------------------
I used SD-Leu-His for all of my selective media.  The sgRNA gene only repairs 
Leu, but I also want to keep up the selection for the YFP gene, which repairs 
His.  The YFP gene causes a growth defect, so cells that don't have it can take 
overtake the population.

.. literalinclude:: 20170823_yeast_library_prep.txt

:ref: _neo_yeast_screen:

Screen ux with tdh1
-------------------
1. Scrape the library off the plates.  For each plate:

   - Pour ~5 mL YPD on the plate.

   - Use a cell spreader to scrape all the cells off the plate and to resuspend 
     them in the YPD.

   - Immediately pour the resuspended cells into a clean flask.  (If you wait, 
     the YPD will soak into the plate and you'll need to scrape the cells off 
     again.)

2. Measure the OD of the resuspended cells.

   I diluted the cells 100x (990 μL YPD + 10 μL cells) and measured an OD of 
   0.2014, meaning the OD of the whole culture (100 mL because I started off 
   with 50 mL YPD in the flask, then added about 50 mL more as I resuspended 
   the cells) was 20.14.  The OD I actually measured was within the linear 
   range of the spectrophotometer (i.e. <0.5), so I trust that it's reasonable 
   and that I chose the appropriate dilution.

3. Make a glycerol stock of the resuspended library cells.

4. Also pick a `tdh1 on` colony and a `tdh1 off` colony and resuspend each in 
   18 μL YPD.

5. Prepare media with and without the ligand.

   - Mix 30 mL YPD with 1 μL 3.6 mM estradiol
   - Divide the YPD + estradiol into 2 14 mL aliquots.
   - To the first aliquot, add 50.89 μL water.
   - To the second aliquot, add 50.89 μL 25 mg/mL neomycin (100 μM final).
   - Label 6 cultures tubes, for 3 strains (on, off, ux) times 2 conditions 
     (with and without neomycin).
   - Use 4 mL media for each culture.

6. Inoculate each culture with 8 μL resuspended cells.

   I decided that it was not worth growing an overnight culture.  As I 
   understand it, there are two purposes to growing overnight cultures.  The 
   first is to get the all cells in the same metabolic state (i.e.  stationary 
   phase).  I think this is more important when studying biology than when just 
   expressing a fluorescent protein off a strong promoter.  I just care that 
   the cells ultimately divide enough to dilute away any YFP that was there in 
   the beginning.
   
   The second is to get larger cultures that all have roughly the same 
   concentration of cells, by virtue of being saturated, so that new cultures 
   can be started from a consistent number of cells.  Resuspending the library 
   and the controls solves the problem of starting apo and holo cultures with 
   the same number of cells (which is important).  I might not have the same 
   number of cells in the control and library cultures.  But since the controls 
   are only needed to help draw the gates for this experiment, it's not a real 
   problem if they grow a little differently that the library (and experience 
   says they'll be very similar anyways).

   The advantage of not growing an overnight culture is that it every growth 
   step increases the bias due to differences in growth rates, so avoiding the 
   overnight culture reduces bias.

   I chose 8 μL to try to reach OD 0.04 (i.e. approximately a 250x dilution 
   from a regular OD=10 overnight culture).  But in retrospect, that may not 
   have been enough to get full coverage of the library (assuming the whole 
   library was actually transformed).  According to someone on the internet, 
   there are 3×10⁷ yeast cells/mL at OD=1.  Let's assume that that's at least 
   in the right ballpark.  I took 8 μL at OD=20, which should be about 5×10⁶ 
   cells.  The ux library has about 3×10⁵ members, which means I got about 15x 
   coverage.  That on the very low end of having enough coverage.  In the 
   future, I might want to subculture 80 μL into 40 mL to be more sure that I'm 
   getting the whole library.

7. Incubate the cells at 30°C for 23h with shaking at 225 rpm.

8. Transfer the cells into PBS

   - Spin at 3500g, 5 min, 4°C
   - Discard the supernatant and add 4 mL PBS.
   - Vortex to resuspend.

   In retrospect, I don't think this step was worth it.  There's nothing wrong 
   with having a little media go through the sorter; this is how I've done 
   literally all of my other sorts.  Plus it took 15 minutes, and if anything 
   vortexing the cells before sorting them might cause fewer to survive.  So I 
   don't think I'll do this again.

9. Dilute the cells into PBS for sorting.

   I diluted 10 μL of cells into 1 mL of PBS (20 μL into 2 mL for the 
   libraries).  I was expecting this to give me an event rate of 1000 evt/sec, 
   but I actually got about 3000 evt/sec.

10. Screen for cells that repress YFP without ligand.

   Gate: 0.2% most on.  This covered about 75% of the on control population.  
   0.1% of the cells in the off control fell in this gate, so the best I can 
   hope for is a 2x enrichment.

   I also added a gate in SSC-W vs SSC-H space to identify singlets.  This is 
   in addition to the gate in FSC-A vs SSC-A space I'd been using to identify 
   living cells.

   I sorted the cells at a rate of 3314 evt/sec for 0:12:38 into 1 mL YPD.  I 
   ultimately collected just 5334 cells.

11. Incubate the sorted cells (and the controls) at 30°C for 48h with shaking 
    at 225 rpm.

12. Prepare media with an without neomycin as in step 5.

13. Inoculate each culture as in step 6.

14. Incubate the cells at 30°C for 24h with shaking at 225 rpm.

15. Dilute 10 μL of each culture into 1 mL PBS.

16. Screen for cells that express YFP with ligand.

   Gate: 0.4% most on.  This basically coincided with the off control 
   population.

   The neo population was actually shifted more towards the "on" control than 
   the apo population.  I'm suspicious that this may just have been a gradual 
   shift over time, because when I rerecorded the neo population after about 
   half and hour of fiddling with the controls and such, the population had 
   shifted from 80% on to 90% on.

17. At this point I abandoned the screen, because the transformation was so bad 
    and the populations in the first two FACS sorts didn't look promising (they 
    looked too homogeneous, not enough smear).


Results
=======

Top10 transformations
---------------------
.. electrotransformation::

   tdh1 neo ux 3,2:
      conc: 105.2 ng/μL
      colonies: 49 3 0 0
      recover: 1060 μL

   tdh1 neo ux 4,3:
      conc: 178.9 ng/μL
      colonies: x 16 1 0
      recover: 1032 μL

   tdh1 neo ux 5,4:
      conc: 190.2 ng/μL
      colonies: x 28 0 1
      recover: 3159 μL

The sequencing for the `neo ux` libraries had a lot of mixed peaks.  I did 
forward and reverse sequencing, so I know that the linkers themselves are 
correct, but I think there are probably a lot of errors where the primers meet.  
I'd probably have to order PAGE-purified primers if I want to get around this, 
but I don't think I will.  The problem seems to be the worst for `ux 3,2`, and 
I'm not at all worried about getting good coverage of that library (it only has 
1024 members), so I think the cost outweighs the benefit.

.. electrotransformation::

   tdh1 neo rhi 4,4:
      colonies: x 76 2 2
      recover: 2085 μL

   tdh1 neo rhi 4,5:
      colonies: x 58 3 1
      recover: 3130 μL

   tdh1 neo rhi 5,4:
      colonies: x 33 4 0
      recover: 3122 μL

   tdh1 neo rhi 5,5:
      colonies: x 68 10 2
      recover: 4156 μL

The sequencing for the `neo rhi` libraries was good.  For some reason, the 
forward sequencing runs worked better than the reverse ones, but that doesn't 
really matter.  I accidentally mixed together the 45 and 54 sublibraries, so 
they sequenced with mixed peaks, but with careful inspection the aptamer and 
linker regions appear to be correct for both sublibraries.  

Transform ux into yBMH127
-------------------------
The transformation did not work well.  I counted 459 big colonies on one plate, 
times 9 plates is 4131 transformants total.  There were perhaps 10x more small 
colonies, but I'm not really sure if they were transformed or not.  Even if 
they were, I don't think they could've accounted for more than 10% of the total 
cell population.

I don't really expect to find anything with a library this bad, but I'm going 
to run it through the whole pipeline anyways.  I still don't know why my cells 
mysteriously died last time, and I'm hoping that problem will just go away.

I've always been suspicious of the way I get big and small colonies with this 
competent cell prep.  I'm hoping that I'll get better results with the 
healthier strain Ben made for me, but if not I'll have to go back to the Deuber 
lab chemically competent prep.


References
==========
.. [Weigand08] Weigand et al. Screening for engineered neomycin riboswitches 
   that control translation initiation.  RNA (2008) 14:89-97.

.. [Briner14] Briner et al. Guide RNA functional modules direct Cas9 activity 
   and orthogonality.  Mol Cell (2014) 56:333-339.
