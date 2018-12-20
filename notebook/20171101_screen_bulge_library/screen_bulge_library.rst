********************
Screen bulge library
********************

I'm not yet finished screening theo/ux and theo/rhi in yeast, but the initial 
results aren't promising.  I might expect to have more luck with an upper 
stem/bulge library, since that's where I gotten my best in vitro and in vivo 
results.  The problem has been that I haven't had a way to switch the spacer 
with these libraries --- the bulge is only 6 base pairs away from the spacer 
(not nearly long enough for a PCR primer) --- so I end up getting 
spacer-dependent sensors.

.. figure:: spacer_lower_stem.svg
   :align: center
   :width: 250px

Tonight, it occurred to me that I might be able to get around this by doing a 
golden gate assembly using a Type IIS restriction enzyme with a long offset 
between its recognition and cleavage sites.  The basic approach would be the 
same as I'm already doing for yeast: PCR amplify the whole gene to add 
restriction sites on either end, make a backbone with the same sites, then do 
Golden Gate assembly.

Planning
========

Picking a restriction enzyme
----------------------------
10/31/17:

I searched through the following list looking for enzymes two qualities: as 
many bases as possible between their recognition and cleavage sites, and a 
large an overhang as possible:

https://www.neb.com/tools-and-resources/selection-charts/type-iis-restriction-enzymes

BtgZI looked like the best candidate with a 10bp offset and a 4bp overhang.  
All the enzymes with ≈20bp offsets seem to require SAM modification (I'm not 
totally sure what that is, but I don't think I'll have it), and all the enzymes 
with 12--14bp offsets have only 2bp overhangs.  Plus, BtgZI was one of the 
relatively few enzymes labeled as having been successfully used for Golden Gate 
reactions.

The 10bp overhang for BtgZI means that I can have a 16bp primer leading up to 
the restriction site.  This primer would have Tm=53°C and GC%=38, both of which 
are reasonable.

Library design
--------------
11/1/17:

The rb library worked well in E. coli (except for being spacer dependent), but 
it's too big for yeast.  With yeast I can only expect to get 2×10⁵ 
transformants (8.8 positions), while the complete rb library had 6×10⁷ members 
(12.9 positions).  So I need to find way to make the library smaller.

One obvious way to reduce complexity is to flank the aptamer with a 5'G and a 
3'C.  Every forward and backward design I isolated from the rb library had a 
canonical base pair flanking the aptamer, and most of the time it was a 5'G and 
a 3'C (although 5'C and 3'G was more common for backward designs):

==  ==  =======  ========
5'  3'  Forward  Backward
==  ==  =======  ========
G   C   14       2
C   G   1        3
A   T   2        1
T   A   0        1
==  ==  =======  ========

Another way to reduce complexity would be to make fewer sublibraries.  I looked 
at my old results to see which sublibraries were most enriched for the forward 
and backward designs.  Numbers in parentheses are normalized to the size of the 
sublibrary in question.  One conclusion is that forward sensors prefer 
asymmetric linker lengths, while backward sensors prefer symmetric lengths.  So 
if I were to only select for forward sensors, I could leave out rb/6/6 and 
rb/5/7.  (I think this makes sense because the nexus libraries are better for 
backwards designs anyways.)  Another conclusion is that most of the forward 
hits came from sublibraries with 4 nucleotides in the 5' linker, so I could 
probably just make rb/4/8, rb/4/7, and rb/4/6.

=======  =======  ========
Library  Forward  Backward
=======  =======  ========
rb/4/8   6 (6)    0
rb/5/7   4 (4)    0
rb/6/6   1 (1)    4 (4)
-------  -------  --------
rb/4/7   3 (12)   0
rb/4/6   2 (32)   0
rb/5/6   1 (4)    2 (8)
rb/5/5   0        1 (16)
=======  =======  ========

Those two strategies get me down to a complexity of 1×10⁶.  I could get down to 
3×10⁵ by dropping rb/4/8, but my instinct is to keep it.  I think I can 
probably do enough transformations in parallel to get up to ≈50% coverage, and 
assuming that I'm really sampling base-pairing space, that's probably good 
enough.

I ended up calling this library rbi rather than rb, because it would've been 
more work than it was worth to move the rb library to the Dang scaffold.  I 
kept the number the same for rb and rbi even though rbi also fixes the base 
pair nearest the aptamer, so the libraries I will make are:

- rbi/4/8 (N=10)
- rbi/4/7 (N=9)
- rbi/4/6 (N=8)

Designing primers
-----------------
11/1/17:

First, I need primers for the library itself:

.. literalinclude:: 20171101_clone_into_sgrna.txt

Second, I need primers for amplifying the library off of the yeast genome with 
BtgZI sites and for installing BtgZI sites in the entry vectors.  These I 
designed manually and tested in snapgene:

:download:`manual_primers.xlsx`


Methods
=======

Inverse PCR
-----------
11/14/17:

I used a 4 min extension for the PCR, not 2 min.  When plating dilutions after 
the electrotransformation, I noticed that the plates were pretty dry (i.e. the 
20 μL dilutions soaked into the plate in only ≈30 min).  I'm worries that this 
could negatively affect how many colonies survive.

.. literalinclude:: 20171114_library_prep.txt

A small (≈300 bp) unexpected product came out of the PCR reaction.  I'm not 
going to worry about it, because it's too small to contain the antibiotic 
resistance genes, so it won't get transformed.

.. figure:: 20171115_rbi_pcr.png
   :width: 400px

   PCR products for rbi sublibraries.  ≈0.75% agarose/TAE/GelRed gel.  From 
   left to right, the lanes are: GeneRuler 1 kb ladder, rb1/4/6, rbi/4/7, 
   rbi/4/8.  The major product is 5.8 kb.
   
Transform into Top10
--------------------
11/17/17:

The transformations worked really well.  I easily got full coverage of all the 
sublibraries.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL

   tdh1 rbi 4,6:
      colonies: x x 79 6
      recover: 1035 μL
   tdh1 rbi 4,7:
      colonies: x x 111 10
      recover: 2018 μL
   tdh1 rbi 4,8:
      colonies: x x 49 3
      recover: 8162 μL

Transform into yBMH139
----------------------
11/22/17:

Transform the libraries into yBMH139 following the Gietz2007_ protocol.  I used 
9.16 mL overnight culture, began at an OD of 0.487 (10 × 0.0487), ended at an 
OD of 2.207 (10 × 0.2207) after 3h53, and linearized the library in the 
following reaction:

- 18.76 μL water
- 50.74 μL 2365.6 ng/μL DNA
- 8.50 μL 10x CutSmart buffer
- 7.00 μL 20 U/μL NotI-HF

I plated the cells onto 30 145 mm plates using beads.  Using beads was a 
mistake because I lost a lot of cells --- maybe as many as half my 
transformants --- when discarding the beads into ethanol.  Letting the plates 
sit for a while so the cells could soak in wouldn't've worked, because many of 
the plates had water from the lids that had been sitting on the agar all day 
without soaking in.  Bear in mind that the counts in the table below are from 
the dilutions, which didn't involve the beads at all.  So my actual number of 
transformants is probably worse than this.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL
   :recover: 12000 μL

   tdh1 rbi:
      colonies: 12 2 0 0
      library_size: 65536 + 262144 + 1048576

This transformation wasn't very good (8e4), but it also wasn't that far out of 
line with the other transformations I've done (Dueber: 2e5 and 9e4, Gietz: 5e5 
and 9e4).  Still, this was worse than usual, not even considering that I may 
have lost a significant number of transformants to the beads.  I was able to do 
5x better with the tdh2/rhi library, so it's within reason that I could get 
that efficiency again, even if there wasn't anything I knowingly did 
differently between the two preps.  An improvement to 25% coverage would be 
much better, so I'm going to at least try repeating this transformation.  Maybe 
I'll do the 60x scale this time, although I probably stay at 120 μg DNA because 
otherwise I'd have to prep more.  I do need to wait for more SD-Leu, though.  
Right now I'm out and I can't make more plates.

Transform into yBMH139 again
----------------------------
11/28/17:

I didn't get enough transformants last time, but some other transformations 
with the same protocol would've gotten enough, so I just decided to repeat the 
same Gietz2007_ protocol as before with a few minor changes:

- I did the 60x prep instead of the 30x prep, but I only used 120 μg of DNA 
  because I didn't have 240 μg.

- I made fresh 50% PEG₃₃₅₀ the day before.  This was pretty difficult: Most 
  protocols agree that the precise ratio of PEG to water is very important, so 
  I tried to use a graduated cylinder to get it just right, but that meant 
  transferring the PEG between a beaker and a graduated cylinder a couple 
  times, and PEG is very viscous, so every time I lost some PEG.  If I do this 
  again in the future, I'll probably do everything in a 50 mL Falcon tube.  
  Maybe before I start I can measure 50 mL water in a graduated cylinder, pour 
  in into a Falcon tube, and mark the level, so I can just fill up to that once 
  I add the PEG.

- I made 34 plates from 3L of SD-Leu.

- I used a cell spreader to plate the cells, rather than beads.  (See the 
  discussion from last time for the problem with beads.)

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 40 μL
   :recover: 13840 μL

   tdh1 rbi:
      colonies: 11+17 2+1 1 0
      library_size: 65536 + 262144 + 1048576

My titer plate was absolutely covered in mold colonies, so I may have counted 
fewer colonies than there should've been.  I think the problem is that I tried 
to be clever about drying out the plates by putting a paper towel around the 
sleeve to absorb any extra water, but the towel got covered in mold (I threw it 
out once I saw that) and apparently the plates did too.  

That said, I picked fairly representative looking plate and counted 932 
colonies.  Extrapolating that to the whole library (932 cfu / 400 μL * 13840 
μL) and I get 3.2×10⁴ colonies, which is 3x fewer than I got from my titer.  I 
trust the count more that the titer.

Screen tdh1/rbi
---------------
12/4/17:

- Resuspend library and start overnight cultures.

   - I decided to combine my two transformations, because I didn't get very 
     many transformants with either one.  Since the first transformation had 
     incubated at 30°C for longer, the colonies on those plates were bigger.  
     This made it especially important to accurately count the number of 
     transformants in both libraries, so that I could evenly combine the two 
     sublibraries.

     Instead of trusting the titers, I decided to directly count the number of 
     colonies on a few plates and extrapolate from those.  I'd already done 
     this for the second transformation, and got 32,247 colonies.  For the 
     first transformation, there seemed to be two families of plates.  The 
     first had darker agar and more colonies.  The second had lighter agar and 
     fewer colonies.  I'm not sure, but I think the darker plates were the 
     Takara SD-Leu agar packets and the lighter plates were the Sunrise Science 
     powders.  In the future, I might want to order more of the packets, since 
     they seemed to support more survival.  Anyways, I counted the colonies 
     from one representative plate from both families and multiplied by the 
     number of plates in that family (Takara: 962×18, Sunrise: 494×13).  It 
     added up to 23090 colonies.

   - Add 5 mL YPD to each of the library plates, and use a cell scraper to 
     resuspend the cells.  Pour the resuspended cells off the plates and into a 
     500 mL Erlenmeyer flask.  In retrospect, I should've resuspended the cells 
     in SD-Leu.

   - Measure the OD of the two resuspended transformations:

     .. od::
        :dilution: 1000x

        11/22/17: 0.1375
        11/28/17: 0.1160

   - Calculate how to combine the libraries.  I wanted at least 1 mL, so I 
     would have enough to start an overnight and make a glycerol stock.  I 
     ultimately decided to mix:

     - 604.1 μL 11/22/17 library
     - 1000.0 μL 11.28/17 library

   - Library overnights: 50 mL SD-Leu, 25 μL combined library.  I decided to 
     use SD-Leu to keep the number of cells without the sgRNA insert low.  The 
     amount of library to add was pretty arbitrary.  I used 48 μL for the ux 
     and rhi libraries, but this mixture was extremely concentrated (i.e.  
     OD≈100), so I decided I could use a little less.  I didn't want to add so 
     many cells that they would be dying by the morning, but other than that I 
     figured the more I added the less chance there would be for biases due to 
     growth.

   - Control overnights: 1 mL SD-Leu, cells scraped from glycerol stock.

12/5/17:

- Prepare fresh theophylline.

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

   - Gate: holo culture, 1.5% most on (vs 1.0% apo population)

   - Sort for 15m at 1000 evt/sec.  Collect cells in 1 mL YPD.

   - I drew a pretty generous gate (it was nearly touching the off population), 
     so I didn't want to collect cells for too long, because I was worried that 
     if I got something like 100x coverage, at least a few cells for every 
     variant might get though.  So I decided to only sort for 15 min.

- Start overnight cultures (without adding more YPD).

12/7/17:

- Prepare fresh theophylline.

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

   - Gate: apo culture, 5.8% most off (vs 3.9% holo population)

   - Sort for 10m at 1000 evt/sec.  Collect cells in 1 mL YPD.

- Start overnight cultures (without adding more YPD).

Swap spacer
-----------
2018/02/06:

I scraped cells from glycerol stock #466 to get cells for the colony PCR.  The 
insert I added to the ligation reaction was 20.1 ng/μL, not ≈50 ng/μL.  If I 
were to do this again, I'd probably do 100--150 μL of PCR to get closer to the 
indicated amount of insert.

.. literalinclude:: 20180207_swap_spacer.txt

2018/02/07:

This is another bad-but-probably-good-enough transformation.  I made fresh 
competent cells this time, because the cells I had been using were probably 
about 6 months old, but it didn't help at all.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 40 μL
   :recover: 4100 μL

   tdh2 rbi:
      conc: 48.2 ng/μL
      colonies: 21 0 0 0
      library_size: 1000

2018/02/08:

This time the sequencing looks like at least most of the DNA is from the 
library, which is good enough.  This cloning was pretty rough: nothing worked 
well, every was just "good enough".

.. figure:: tdh2_rbi_sequencing.png

Troubleshooting
===============

Swap spacer --- Just got entry vector
-------------------------------------
12/9/17:

I used a 60°C annealing temperature for the colony PCR like the protocol says, 
but that was a mistake because the BtgZI primers are shorter and were designed 
for Ta=54°C.  In the end it wasn't a problem, though, the PCR worked really 
well at 60°C.  In fact, if I ever do this in the future, I'd probably keep Ta 
at 60°C because higher annealing temperatures help discourage off target 
products.

The protocol also still has the restriction digest for BsaI, and should be 
different for BtgZI.  In particular, mix 7 μL backbone plasmid, 1 μL CutSmart 
buffer, and 2 μL 5 U/μL BtgZI; incubate at 60°C for 1h, then 80°C for 20 min; 
gel purify for a 0.6% gel run at 80V for 1h30; elute in 25 μL EB.

.. literalinclude:: 20171209_swap_spacer.txt

The colony PCR worked very well:

.. figure:: 20171212_tdh1_rbi_colony_pcr.png
   :width: 400px

   2% agarose/TAE/Gelred gel, 100V, 60m.  From left to right: 2 μL GeneRuler 
   100 bp DNA Ladder, 3 μL of rbi colony PCR product after PCR cleanup and 
   elution in 25 μL water with 1μL 6x OrangeG.  The expected product is 180 bp 
   (the bottom two ladder bands are 100 bp and 200 bp, respectively).

The backbone linearization also worked well:

.. figure:: 20171212_linearize_tdh2_btgzi.png
   :width: 400px

   0.6% agarose/TAE/GelRed, 80V, 90m.  I had to change the color threshold to 
   get the ladder to appear, because the backbone band is so bright.  The 
   expected product is 5694 bp and the topmost bright ladder band is 6000 bp.

This wasn't a very good transformation, but it didn't need to be.  I think I 
only have a couple hundred sequences left in the library.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 40 μL
   :recover: 1000 μL

   tdh2 rbi:
      colonies: 42+54 6+6 2+0 0+0
      library_size: 1000

12/15/17:

Unfortunately, the sequencing showed that I ended up with nothing but entry 
vector.  In this light, it's pretty surprising to me that I got as many 
colonies as I did.  I gel purified the entry vector, and I also didn't see any 
uncleaved vector on the gel (although the cleaved band is very large, so maybe 
it's obscuring something).  So I don't know where this entry vector came from.  
Did it never get cleaved in the first place, or did it somehow get re-ligated?  
I definitely should've successfully removed most if not all of the 66 bp 
fragment that was cut out of the entry vector.

Retransform into BMH139 --- Just got entry vector
-------------------------------------------------
12/14/17:

Transform the libraries into yBMH139 following the [Gietz2007]_ protocol:

   - I cast SD-Leu plates the day-of, because I didn't plan far enough ahead to 
     do it the day before.  I only made 10 plates because 30 has been too many 
     for all my previous transformations.

   - I miraprepped the DNA from the Top10 transformation, also on the day-of.  
     Yield: 2327.9 ng/μL.

   - I setup the NotI digestion as for ux and rhi: mix 17.95 μL water, 120 μg 
     DNA (51.55 μL at 2327.9 ng/μL), 8.5 μL 10x CutSmart buffer, and 7.0 μL 20 
     U/μL NotI-HF; incubate at 37°C for 1h, then at 65°C for 20 min, then hold 
     at 12°C.

   - The day culture began at OD 0.494 (10×0.0494).

I did transformation before confirming the sequence of the library, and since 
that confirmation ultimately failed, this transformation was futile.

Swap spacer --- Mixed peaks
---------------------------
2018/01/22:

I left the backbone plasmid (27, "tdh2: BtgZI") out on my bench for the last 
month.  It's probably fine, but since I'm in debugging mode I'm going to 
re-transform, re-miniprep, and re-sequence it just to make sure.

.. update:: 2018/01/25

   I re-sequenced the plasmid with both forward and reverse primers.  Both 
   traces came back with the expected sequence everywhere, including the two 
   BtgZI sites.  I also got a similar yield as before with my miniprep (30 μL 
   ≈900 ng/μL in EB), so I think my insert vector is correct.

2018/01/25:

I think the mistake I made last time was trying to do a golden gate assembly 
rather than simple restriction cloning.  The problem is that BtgZI has a very 
high optimal temperature, so using BtgZI and T4 DNA ligase in the same reaction 
is not a good idea.  (Last time I alternated between 42°C and 16°C.  I know 
that works for BsaI, but my guess is that 42°C just isn't hot enough for 
BtgZI.)  So this time, I added a second BtgZI digest step for the insert (after 
doing the PCR cleanup), and replaced the golden gate step with an overnight 
16°C incubation (with T4 DNA ligase only).  I didn't gel purify the insert; 
since it's not coming from a vector I don't need to worry about removing the 
backbone.

I didn't have fresh yeast anymore, so I scraped what looked to be about 5 μL 
from a glycerol stock.  I wanted to use a little more than the protocol calls 
for because the glycerol stock is a little diluted with glycerol.

When I did the gel extraction, in retrospect I would've liked to have cut a 
smaller piece.  The piece I cut just encompassed the whole band, but the band 
is really big, and I think I would've done better to just cut out the middle of 
the band.

If I have to do this again, I'm thinking about trying to eliminate a spin 
column step by doing the restriction digest of the insert directly in the PCR 
buffer.  NEB has a `good page`__ describing the pros and cons of this.  The 
drawbacks are that BtgZI doesn't cleave very well in Q5 buffer (≈25%), the 
polymerase might fill in the sticky ends, and the primers might compete with 
the insert for the restriction enzyme.  NEB recommends adding the restriction 
enzyme's buffer (e.g. CutSmart) to 1X, but their data was collected without 
that.

__ https://www.neb.com/tools-and-resources/usage-guidelines/activity-of-restriction-enzymes-in-pcr-buffers

.. literalinclude:: 20180125_swap_spacer.txt

Comparing this gel to the one I made the first time I did this, I can safely 
say that the PCR worked both times.  Previously I didn't do a control reaction, 
and James pointed out that my band could've been some sort of primer dimer.  
But this gel clearly shows the primers and the product, and the product is in 
the exact same place as before (and right at the expected size).  A big 
difference is that my yield was much worse this time.  (Last time, it seems 
like all of the primers were incorporated into the products.)  My initial 
thought is that this is somehow attributable to using a glycerol stock for my 
template.

.. figure:: 20180125_amplify_rbi.png
   :width: 400px

   2% agarose/TAE/Gelred gel, 100V, 60m.  From left to right: 2 μL GeneRuler 
   100 bp DNA Ladder, negative control PCR (+ primers, − template), rbi colony 
   PCR.  After a PCR cleanup, my yield of colony PCR product was 25 μL × 8.7 
   ng/μL.  The expected product is 180 bp (the bottom two ladder bands are 100 
   bp and 200 bp, respectively).

Again, comparing this gel to the one I made the first time I did this, I can 
safely say that the restriction digest of the backbone worked both times.  
Previously I didn't run the undigested plasmid, and even though the big band 
seemed to have the right molecular weight, it's hard to know how circular DNA 
will run.  I am I little concerned that I cut too generous of a piece out of 
the gel, and might have gotten some of the upper control band.  But it any case 
clearly most of the DNA was digested, and I'm confident I cut out most of the 
DNA that wasn't.
   
.. figure:: 20180125_linearize_tdh2_btgzi.png
   :width: 400px

   0.6% agarose/TAE/Gelred gel, 80V, 90m.  From left to right: Digested 
   backbone (7 μL), undigested backbone (1 μL), GeneRuler 1kb DNA Ladder.  The 
   plasmid is 5694 bp and the topmost bright ladder band is 6000 bp.  I 
   manipulated the colors in this image to make the ladder and the undigested 
   control visible.

This is not a good transformation, but I think it's good enough.  I only 
managed to transform 5×10⁴ variants into yeast in the first place, so I'm 
pretty confident that I have less that 1×10⁴ variants left.  If I were to do 
this again, though, I'd probably try to get more insert by increasing the 
number of colony PCR cycles to 35.

.. electrotransformation::
   :dilutions: 10 ^ 1 2 3 4
   :plate: 20 μL
   :recover: 1000 μL

   tdh2 rbi:
      colonies: 19 2 0 0
      library_size: 1000

The sequencing showed mixed peaks.  Squinting at it, I think there's a roughly 
even mix of library and entry vector.  I think I can do better if I get more 
insert by doing 35 cycles of PCR (I think that's what I did the first time, 
based on how the gel looked), so I'm going to try that.


References
==========
.. [Gietz2007] :doi:`10.1038/nprot.2007.15`


