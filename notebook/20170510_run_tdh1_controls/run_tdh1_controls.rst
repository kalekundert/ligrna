*****************
Run TDH1 controls
*****************

Before I attempt a library screen in yeast, I want to make sure I can get good 
signal for the controls.  This experiment will only include `tdh1 on` and `tdh1 
off`, with literature concentrations of neomycin and tetracycline.

Choice of media
===============
Ben and Andrew advised me to use SDC for this experiment, but the rationale is 
worth discussing.  The alternative is to use YPD, which is actually a richer 
media:

=====  =============
Media  Doubling time
=====  =============
YPD    90 min
SDC    115 min
=====  =============

The problem with YPD is explained well by this paragraph from Bitesize Bio: 
http://bitesizebio.com/24032/top-tips-for-yeast-microscopy/

    Many of the laboratory strains have mutation in adenine pathway (ade-) 
    meaning that they are unable to synthesis adenine themselves. However, in 
    the absence of exogenous adenine they still try to synthesis adenine 
    resulting in the generation of phosphoribosylaminoimidazole, an 
    intermediate in the adenine pathway that fluoresces in response to blue 
    light and will interfere with your GFP signal. There is not much adenine in 
    YPD and there may not be enough in the synthetic defined media you are 
    using. Therefore, if you are working with ade- strains ensure that you 
    supplement your media with extra adenine to prevent accumulation of this 
    fluorescent intermediate. Ideally, if possible you should just avoid the 
    use of ade- strains as even excess adenine is not sufficient to completely 
    prevent autofluorescence.

    Cells, which grow in these media accumulate fluorescent adenine pathway 
    with high autofluorescence intermediate in the vacuole, and this will 
    interfere with your microscopy. A simple solution is to add additional 
    adenine to your media prior to growing cells. Alternatively, buy media with 
    additional adenine in them such as "SC + 40 mg/L adenine".

I don't know if the strain I'm using is ade- or not, so I should ask Andrew or 
Ben about that.  I do know that the SDC I'm using has 10 mg/L adenine, which is 
4x less than the 40 mg/mL that Bitesize Bio article recommends (a book called 
Fluorescent Proteins by Kevin F. Sullivan recommends 20 mg/L).  In any case, 
the strain I'm using right now has the TDH3 promoter in front of RFP, so maybe 
phosphoribosylaminoimidazole fluorescence won't interfere (I looked for its 
spectrum but couldn't find anything).

First Try
=========
1. Start 5 mL overnight cultures of `tdh1 on` and `tdh1 off` in YPD.  
   Incubate at 30°C in a rotator.

2. Measure the OD of the overnight cultures by diluting 20 μL into 980 μL YPD 
   in a cuvette and measuring on the spectrophotometer.

   .. od::
      :dilution: 50x

      tdh1 on: 0.2360
      tdh1 off: 0.0829

3. Make 10 mL SDC + estradiol (E2)

   The estradiol stock I received from the El-Samad lab is 3.6 mM, and the 
   working concentration is 125 nM.  Technically that's a 2.88×10⁴ dilution, 
   but I think there's probably some rounding in the stock concentration such 
   that it's actually a 3×10⁴ dilution.  That would be 0.333 μL for 10 mL 
   media.  It's probably better to do two 173.2x dilutions: 1 μL into 172.2 μL 
   water, then 57.74 μL of that into 10 mL media.

4. Dilute the overnight cultures into the SDC media.

   I want the yeast to be in log phase when I measure them.  According to 
   someone on the internet, log phase corresponds to OD 0.3--0.8 (0.4--0.6 if 
   you're being careful) for yeast.  I figure that it makes sense to shoot for 
   OD 0.6, since that's solidly in log phase, and there should still be enough 
   cells that I won't have trouble getting enough events.

   Ben tells me that for this strain the lag time is 90 min and the doubling 
   time in SDC is 115 min.  I'm planning to grow the yeast for 8h, because 
   that's as late as I want to stay tonight.

   .. math::

        C   & = C_0 \cdot 2^{(t - t_\mathrm{lag})/t_{2x}} \\
        0.6 & = C_0 \cdot 2^{(8\mathrm{h} - 90\mathrm{m}) / 115\mathrm{m}} \\
        C_0 & = 0.057 \\

   I'm want to grow the cells in 1 mL media (arbitrary decision), so I need to 
   add the following volumes of overnight culture:

   ========  ======  ========  =========
   Strain        OD  Dilution  Inoculate
   ========  ======  ========  =========
   tdh1 on   11.800    206.4x   4.846 μL
   tdh1 off   4.145     72.5x  13.796 μL
   ========  ======  ========  =========

5. Grow the cells at 30°C for 8h in a rotator.

   I don't really think that 8h is long enough.  With the lag and doubling 
   times mentioned above, there will only be 3.4 doublings in 8h.  Since all 
   the cells should be expressing RFP to begin with, even with perfect 
   repression I would only expect a :math:`2^{3.4} = 10.55\times` change in 
   fluorescence.

   It's worth noting that I'm deviating from the protocol than Ben and Andrew 
   use.  They grow the yeast in two steps:

   - Dilute the overnight culture 1:100 into SDC + estradiol.
   - Grow the culture for 3.5h, at which point it should be at OD 0.4.
   - Dilute the culture to OD 0.1 (4x) into SDC + estradiol ± theophylline.
   - Grow for 5--6h, at which point it should be around OD 0.9 (late log 
     phase).
   - Measure fluorescence by flow cytometry.

   Ultimately, they grow the yeast for 8.5--9.5h.  That's 3.7--4.2 doublings, 
   but only 2.6--3.1 with theophylline.  I'm not that far off what they do, but 
   I'm not really convinced it's enough.  It might be worth growing the cells 
   overnight to see if that improves the dynamic range.

   It's also worth noting that Ben tried putting a degron on the fluorescent 
   protein.  I remember him showing me that it slightly improved dynamic range 
   (while reducing overall signal), but I can't remember any more detail than 
   that right now.  This seems like a promising direction, though.

7. Dilute the yeast so they can continue growing in log phase overnight.

   I'm diluting the cells at 9:00, and I don't expect to get to them until 9:00 
   tomorrow morning, so I need to dilute them such that they reach OD 0.6 after 
   12h.  Assuming that there will be no lag phase (because the cells should 
   never leave log phase) and that the doubling time is still 115 min, I need 
   to dilute the cultures to OD:

   .. math::

        0.6 & = C_0 \cdot 2^{12\mathrm{h} / 115\mathrm{m}} \\
        C_0 & = 0.00782 \\

   Assuming the cultures are really at OD 0.6 now (I'll measure them when I 
   actually get to this step), this will correspond to a dilution of 13.04 μL 
   into 1 mL.

The LSRII was broken, so I was unable to collect flow cytometry data for this 
experiment.  Damn.

Second Try
==========
1. Start 5 mL overnight cultures of `tdh1 on`, `tdh1 off`, `tdh1 tet rxb 
   11,1`, and `tdh1 neo rxb 11,1`.

2. Measure the OD of the overnight cultures by diluting 50 μL into 950 μL YPD 
   in a cuvette and measuring on the spectrophotometer.

   .. od::
      :dilution: 20x

      tdh1 on:           0.3870
      tdh1 off:          0.2856
      tdh1 tet rxb 11,1: 0.0073
      tdh1 neo rxb 11,1: 0.3834      

   The tet culture didn't grow very well, which doesn't surprise me because I 
   tried to start it from my sequencing sample instead of a true colony.  I 
   decided to just use the neomycin construct for the rest of the experiment.

3. Make 10 mL SDC + estradiol (see recipe in first try).

   Also make 10 mL SDC + estradiol + 100 μM neomycin.  This is the 
   concentration used by Weigand et al (2008) in their paper on neomycin as a 
   riboswitch.  We have 25 mg/mL neomycin aliquots (of unknown age) in the 
   freezer, so I thawed one of those and calculated how much to add to 10 mL of 
   media to get a 100 μM solution:

   .. math::

      10\,\mathrm{mL} \times
      \frac{100\,\mathrm{μmol}}{1000\,\mathrm{mL}} \times 
      \frac{908.88\,\mathrm{μg}}{1\,\mathrm{μmol}} \times 
      \frac{1\,\mathrm{mg}}{1000\,\mathrm{μg}} \times 
      \frac{1000\,\mathrm{μL}}{25\,\mathrm{mg}} = 
      36.35\,\mathrm{μL}

4. Start cultures in 1 mL of both media.

   =================  ======  ========  =========
   Strain                 OD  Dilution  Inoculate
   =================  ======  ========  =========
   tdh1 on             7.560    132.6x   7.540 μL
   tdh1 off            5.712    100.2x   9.979 μL
   tdh1 neo rxb 11,1   7.668    134.4x   7.433 μL
   =================  ======  ========  =========

5. Rotate at 30°C for 8h (11:45 -- 7:45).

6. Dilute each culture into PBS for flow cytometry.

   The on and off cultures didn't grow very well, so I decided to do two 
   dilutions into PBS: 1 μL cells into 200 μL PBS, and 10 μL cells into 200 μL 
   PBS.

7. Optimize the laser settings on the LSRII.

   This strain has the same fluorescent proteins as my bacteria, so I didn't 
   have to change the channels.  However, I did turn down the power on all the 
   lasers, and switched from using the fluorescent channels (FITC, PE-Texas 
   Red) to the size channels (FSC, SSC) as thresholds.

8. Measure fluorescence on the LSRII.

   .. figure:: 20170518_rfp_neo_controls_8h.svg

   After 8 hours, the difference between the controls was only very slight.  
   This surprised me.  Ben and Andrew do flow cytometry 9h after inducing with 
   estradiol (and only 5h after adding theophylline), but they seems to see a 
   signal.  I wonder if I'm doing something wrong...

9. Keep growing the cultures overnight at 30°C in a rotator.  My original plan 
   was to dilute them such that they'd reach OD 0.6 around 11:00 tomorrow, but 
   these calculations have never been close for me so far.  Instead, since the 
   cultures seemed very thin already, I decided to just put them back in the 
   warm room without diluting them.

10. Measure the OD of the cultures grown overnight.

    .. od::
       :dilution: 20x

       tdh1 on:           0.1434
       tdh1 off:          0.1183
       tdh1 neo rxb 11,1: 0.5425

    In retrospect, it wasn't really surprising that I got stationary phase 
    cultures.  I should've made a few dilutions to try to get one in log phase.

11. Measure fluorescence on the LSRII using the same parameters as last night.

    .. figure:: 20170518_rfp_neo_controls_23h.svg

    The controls are much more distinct after 23h.  In particular, the negative 
    control is about the same as it was, but the positive control shows much 
    better repression.  This supports the idea that the cells need to undergo a 
    number of divisions to sufficiently dilute fluorescent protein that was 
    expressed before the induction of Cas9.

Third Try
=========
1. Grow overnights for `on`, `off`, and `neo rxb 11,1` in the context of 
   BMH127, which has Venus with a degradation tag behind the TDH3 promoter.

   Once again, my `tet rxb 11,1` streak didn't have any colonies.  This is 
   the second time I've had trouble streaking a tet strain.  This time, I just 
   went on with the `neo rxb 11,1` strain.

   I started the overnights at 10:00, and I made them only 2 mL to help them 
   get to saturation before the next morning.

2. Prepare enough SDC + E2 ± 100 μM neomycin and YPD + E2 ± 100 μM neomycin for 
   6 1 mL cultures (3 in the morning, and 3 to dilute into in the evening).  
   The specific volumes differ than above, but the basic recipe is the same.

3. Measure the OD of the overnight cultures, and dilute them to OD 0.05 in the 
   fresh media (with estradiol):

   =================  ======  ======  =============
   Strain              OD/20      OD  Dilution (μL)
   =================  ======  ======  =============
   tdh1 on            0.5769  11.538           4.33
   tdh1 off           0.4346   8.692           5.75
   tdh1 neo rxb 11,1  0.5911  11.822           4.22
   =================  ======  ======  =============

4. Grow for 8h30 at 30°C.

5. Dilute the cells into PBS for flow cytometry.

   I didn't measure the OD of the cultures, but it was clear by eye that the 
   YPD cultures were denser than the SDC ones.  I diluted 10 μL of each SDC 
   culture into 200 μL PBS, and 2 μL of each YPD culture into 200 μL PBS.  I 
   ran the cytometer at a flow rate of 1 μL/sec, and got event rates of about 
   150 evt/sec for both media.

6. Analyze cell populations by flow cytometry.

   This is where I got stuck.  I noticed that the `off` population (in SDC 
   media) showed no fluorescence in any of the channels I was monitoring: FITC, 
   PE Texas Red, PE (YG), and PE.  The emission and excitation maxima for Venus 
   are 515 nm and 528 nm, respectively.  None of the lasers on the LSRII match 
   those within a few nm.  I even checked the lasers in the El Samad lab's 
   LSRII, and none of them matched especially well either.

   I talked to Andrew about this today, and looked for some papers on how Venus 
   is used for flow cytometry.  Andrew told me that they just use the FITC 
   channel for Venus.  This quote from Marcus13_ corroborates that:

      GFP and YFP are fluorescent proteins that are widely used in various 
      cellular assays (1). The 488 nm blue laser, that is standard on virtually 
      all flow cytometers, efficiently excites both proteins. [...] On most 
      cytometers, GFP/YFP signals are detected using a single band pass filter 
      (usually in the range 500–550 nm).

   The FITC channel on the Lim lab LSRII excites at 488 nm and has a 530/30 
   filter, so it should've worked.  In retrospect, I wish I'd run the rest of 
   the samples last night (maybe there was just something wrong with the SDC 
   `off` culture), but I got too caught up trying to find an appropriate 
   laser.

7. Dilute the cultures into fresh media to grow overnight.  

   I was hoping to catch the cells in log phase this morning, so I diluted the 
   thiner SDC cultures 10-fold and thicker YPD cultures 100-fold.  Ultimately 
   it didn't matter, because the cytometer was booked all morning.  The 
   cultures were mostly around OD 2-4 at 11:00 though, so they probably 
   would've been in log phase around 8:00.

   I also started cultures from BMH126 and BMH127, which are the parent Venus 
   and Venus/degron strains that I cloned my sgRNAs into.  Both strains have 
   Cas9 but no guides, so they should be positive controls for fluorescence.

8. Dilute the cells into fresh media again, this time to get them in log phase 
   around 3:00.  I talked to Andrew this morning, and he said he could do flow 
   cytometry with me at 3:00 to make sure things work in his hands.  I diluted 
   my overnights to OD 0.15 just after 11:00, so they'll have about 4h to reach 
   OD 0.6 (two doublings).

9. Analyze cell populations by flow cytometry.

   =====  =================  ======
   Media  Strain                 OD
   =====  =================  ======
   SDC    tdh1 on            0.3541
   SDC    tdh1 off           0.2316
   YPD    tdh1 on            0.4772
   YPD    tdh1 off           0.5102
   =====  =================  ======

   Andrew did this experiment for me on the El Samad lab LSRII.  I didn't 
   download the data, but he also saw no fluorescence for any of the strains.  
   Ben's going to streak me a new plate and I'm going to bring him the old 
   plate, so he can take a look at it and maybe see if I got the wrong strain 
   somehow.

   The strains didn't quite make it to OD 0.6, which continues the trend of 
   yeast always growing slower than I expect.  Andrew advised me that he 
   usually dilutes yeast to OD 0.1 for flow cytometry, which is way more 
   concentrated than I do for bacteria.  At that concentration, we were getting 
   500-1500 evt/sec at a flow rate of 1 μL/sec.  I also noted Andrew's 
   alive/singlet yeast gate, which roughly goes from 3.5--4.5 on the FSC 
   channel and 3--4.5 on the SSC channel (in log units).  The laser settings 
   for the El Samad cytometer were:

   =====  =======
   Laser  Voltage
   =====  =======
   FSC        225
   SSC        225
   FITC       589
   =====  =======

   The Lim lab LSRII might need different values, but I think this is a 
   valuable starting point.

Fourth Try
==========
Since my last attempt at running these god-damned controls, Ben and I 
determined that the Venus-degron strain (BMH127) wasn't fluorescent for some 
reason, but the plain Venus strain (BMH126) was.  In the interest of time, I 
moved forward with the BMH126.

1. Make 30 mL YPD + estradiol (YE), then use that to make 10 mL YPD + estradiol 
   + 100 μM neomycin (YEN) and 10 mL YPD + estradiol + 100 μM tetracycline 
   (YET).

   - 30 mL YE
      - 30 mL YPD
      - 1 μL 3.6 mM estradiol
      - Mix well

   - 10 mL YEN
      - 10 mL YE
      - 36.35 μL 25 mg/mL neomycin (see calculation in second try)

   - 10 mL YET
      - 10 mL YE
      - 88.89 μL 5 mg/mL tetracycline (see calculation below)

   .. math::

      10\,\mathrm{mL\ YET} \times
      \frac{100\,\mathrm{μmol\ tet}}{1000\,\mathrm{mL}} \times 
      \frac{444.435\,\mathrm{μg}}{1\,\mathrm{μmol\ tet}} \times 
      \frac{1\,\mathrm{μL}}{5\,\mathrm{μg}} = 88.887\,\mathrm{μL\ tetracycline} 

2. Start 1 mL cultures of each strain in each media.

   =================  ======  ======  =========
   Strain              OD/20      OD  Inoculate
   =================  ======  ======  =========
   tdh1 on            0.0272   0.544     200 μL
   tdh1 off           0.5609  11.218      10 μL
   tdh1 tet rxb 11,1  0.5674  11.348      10 μL
   tdh1 neo rxb 11,1  0.5625  11.250      10 μL
   =================  ======  ======  =========

   I'm worried about the positive control.  It grew fine on the SD-Leu 
   transformation plate, but it grew very badly on the SD-Leu plate I struck 
   out and very badly overnight (in rich media).  I never sequenced it; maybe I 
   just chose a bad colony to streak.

   I decided not to think too much about how to dilute the yeast, and just did 
   a 1:100 dilution for all the strains except the positive control.  Andrew 
   told me that he always dilutes his overnights 1:00 without measuring their 
   ODs.  I usually end up calculating to dilute the cells a little more than 
   this (≈1:150), but the cells also usually end up in very early log phase, so 
   maybe this will be better.

   I wasn't sure what to do about the positive control, but I decided to do a 
   1:5 dilution.  That gave me roughly the same number of cells as in the other 
   cultures, but it also significantly diluted the estradiol and the 
   antibiotic.  If I'd been thinking ahead, I could've made 5/4x media and it 
   wouldn't have been a problem.  But I didn't do that, and I didn't want to 
   remake all the media, so I just added 190 μL fresh YPD to each of the other 
   cultures to dilute the estradiol and antibiotics evenly.  
   
   In retrospect, maybe I should've made the 5/4x medias.  The purpose of this 
   experiment is to determine what the dynamic range is, and the concentration 
   of estradiol could be important for that.

3. Rotate at 30°C for 9h (11:00 --- 8:00)

4. Dilute cells into fresh media to grow overnight.

   I'm doing this because I suspect that growing the cells for a very long time 
   could improve my dynamic range by allowing for more doublings.  The cells 
   will grow for about 16h before I can measure them.  Assuming the cells 
   double every 90 min, that means I need to dilute them to OD 0.0003 in order 
   to have them reach mid-log phase when I'm measuring them.  The overnights 
   are about OD600 = 10.0, so I need to add about 0.03 μL to 1 mL media.  I 
   don't really trust these calculations, so I'm going to aim for 0.1 μL 
   instead.  That's a 10,000x dilution, so the best way to achieve that is 
   probably to do 2 100x dilutions.

5. Analyze cell populations by flow cytometry on the Lim lab LSRII.

   The `on` culture grew much more slowly than the others (it never reached 
   stationary phase) and its FSC vs SSC plot looked very unusual.  I think 
   there's probably just something wrong about the colony I picked, so I'm 
   going to restreak a few more colonies and hope that I get one that works 
   better.

   More concerningly, the `off` control was still not fluorescent.  I don't 
   know how this is possible, because I built this strain directly from a 
   culture that Ben and I both saw being fluorescent.  

6. Repeat the experiment with a different `on` colony.

   I struck out two more `on` colonies and they both grew well on plates.  I 
   repeated the flow cytometry experiment with all three `on` strains and the 
   `off` strain.  The two new `on` strains grew just as well as the `off` 
   strain, and looked like yeast in the flow cytometer.  The old `on` strain 
   still grew slowly and looked unusual.  However, I still saw no fluorescence 
   in either control.
   
Fifth Try
=========
I talked to Andrew about the last experiment, because I couldn't think of any 
explanation for why these yeast keep being non-fluorescent in my hands (other 
than grabbing the wrong tube from Ben after we did flow cytometry last week).  
Andrew gave me selective and non-selective plates with BMH126 and BMH127, so I 
could check the parent strains again.  The colonies on the selective plates 
were of notably heterogeneous size.

1. Pick one colony from each plate and inoculate 1 mL YPD.  For the selective 
   plates, I tried to pick a big colony without getting any of the little 
   colonies (although this was probably impossible).

2. Grow for 8h at 30°C with shaking.

3. Analyze cell populations by flow cytometry.

   All four cultures looked identical, and none looked fluorescent.  The 
   average measurement on the FITC channel (in log units) was about 3, whereas 
   I would expect measurements of 5 for fluorescent cells.

   I went to discuss this result with Andrew (again), and he offered to look at 
   the cells under the microscope.  They looked morphologically normal, and 
   weakly fluorescent.  I think this was consistent with my flow cytometry 
   results.  He then gave me the BMH114 and BMH115 plasmids (which contain 
   Venus and Ubiquitin-Degron-Venus respectively) and the yAHN321 parent 
   strain, so I could repeat the Venus transformation myself.

   I sequenced the plasmids and confirmed that they contained the expected 
   sequences.  I then transformed both plasmids and a negative control (i.e.  
   no DNA) into the parent strain, and got lawns for all three.  I thought that 
   this indicated that the parent strain was wrong, but Andrew believes that 
   there's a problem with the His plates.  

Sixth Try --- Jul 18, 2017
==========================
After the last experiment, Andrew gave me the parent strain and both Venus 
plasmids so I could do the transformations myself.  I also did a negative 
control transformation, because I wanted to be certain that the transformation 
worked.  I ended up getting lawns for all three transformations.

I talked with Andrew again, and he speculated that something was wrong with the 
-HIS plates.  This turned out to be the case.  Ben also restreaked some of his 
old glycerol stocks on both YPD and -HIS plates, and found that the YPD 
colonies generally weren't fluorescent while the -HIS colonies generally were.  
From the email he sent me:

   I checked all my freezer stocks and it seems that anything I struck out on 
   YPD had no fluoresence and anything I struck out on SD-His did look good.  
   That is strange - usually I can just streak out on YPD and trust that I have 
   the construct.  

   This indicates to me that

   1) My freezer stocks for this strain are a mixed population with some that 
      have the construct and some that do not. 

   and

   2) The strains with the construct grow more slowly than the strain without 
      so if you remove selective pressure the strain with the reporter drops 
      out of the population. 

   Perhaps the fitness defect could come from overexpressing YFP but that seems 
   unlikely (I feel like we have done that plenty of times with a minimal 
   fitness defect)

   We have had some trouble with the HIS locus in the past, and although we 
   fixed that problem for our standard strain and background vector, we are 
   using a different strain and background vector and perhaps the problem came 
   back.  

   The problem arose before because His3 is right next to a protein Ded1 which 
   seems to cause a growth defect.  It is possible that this construct effects 
   the expression of Ded1 and therefore the fitness.   

   I feel like for now maybe the best thing to do is to restreak freezer stocks 
   onto SD-HIS, and keep an eye out for contamination.   For any 
   transformations into the strain it might be good to use double selective 
   media (i.e. if you are putting things into the leu locus use -His -Leu 
   plates). 

   I am guessing you have already transformed so you might want to try to 
   replica plate onto SD-His plates before picking colonies. 

   Worst case scenario we would want to put the reporter in a different locus 
   or use a vector that doesn't have this problem and make a reporter strain 
   with no growth defect. 

I think these experiments have implications for my library transformations, 
namely that I should restreak my glycerol stock on -HIS plates beforehand and 
use doubly selective media (i.e. SD -HIS -LEU) afterwards.  

In any case, I grew overnight cultures of both the Venus (BMH126) and 
Venus-degron (BMH127) strains from the selective plates.  Both were 
fluorescent, so I transformed `tdh1 on`, `tdh1 off`, `tdh2 on`, and `tdh3 on` 
into BMH127.  (I prefer BMH127 to BMH126 because it's supposed to have better 
dynamic range.  It should also depend less on dilution-by-growth, so I 
shouldn't need to grow it as long.)

1. Pick two colonies from each transformation to restreak on -LEU plates.

   As mentioned above, it would've been better to use -HIS -LEU plates, but I 
   didn't have any.  I picked two colonies because in the past I've had 
   problems with restreaks not growing, but this time they all grew.

2. Make 3 mL overnight cultures in YPD for each strain.  

3. Prepare 10 mL each of YE, YET, and YEN as described in attempt #4.

4. Dilute 10 μL of each overnight culture into 1 mL of each media.

   The overnights all grew about the same amount and were relatively thick, but 
   I didn't measure their ODs.  I just did a 1:100 dilution because I'm coming 
   to the feeling that that's usually close enough.

5. Incubate at 30°C for 10h.
   
   Just after I started the cells growing, I realized that my YPD had some mold 
   growing in it.  I didn't have time to setup the experiment again, so if I 
   see no fluorescence (especially in conjunction with weird FSC vs. SSC 
   distributions), this could be the reason.  That said, the mold was not 
   spread through the whole media -- there was just one fuzzy sphere at the 
   bottom of the bottle -- so it's possible it won't affect my data.

6. Analyze cell populations by flow cytometry on the Lim lab LSRII.

   .. figure:: 20170718_venus_controls.svg

   In 10h, I see about a 15x change in fluorescence with and without Cas9.  For 
   comparison, with the RFP strain I saw a 1.5x change after 8h and a 11x 
   change after 23.  So this strain does have a better dynamic range and a 
   better "time-to-signal" than my old strain.  (I'm not sure if it was worth 
   two fucking months, though.)

   Another positive is that all 3 spacers seem to work similarly.  In fact, 
   `tdh3` might be the best.

   The peaks don't have the nice Gaussian shape I'm used to seeing.  You can 
   see why this is if you look at the scatter plots: some of the cells sag 
   below the GFP/SSC diagonal.  This spreads out the peaks due to the 
   normalization and the log-scale binning.

   One issue is that `tet` seems to affect the controls.  Both `on` and `off` 
   were a little brighter with `tet`.  This may be due to a growth defect: the 
   `tet` cultures seemed to be about half as concentrated, going by the event 
   rate on the flow cytometer.

Seventh Try --- Jul 19, 2017
============================
I want to try growing the cells for 24h, to see if that improves the dynamic 
range.  It did for the RFP strain.  This strain also clearly has a growth 
defect, so it might benefit from having more time to grow.  

1. Make 3 mL overnight cultures as in attempt #6, but grow them for a full 24h 
   to allow them the become fully saturated.

3. Prepare 10 mL each of YE, YET, and YEN as described in attempt #4.

4. Dilute 10 μL of each overnight culture into 1 mL of each media.

5. Incubate at 30°C.

   I put the cells in the incubator at 7:30 PM on Jul 19, 2017.

6. Analyze the cells by flow cytometry after 17h (at 12:30 on Jul 20, 2017):

   I diluted 10 μL of cells into 200 μL PBS for the flow cytometer.

   .. figure:: 20170720_venus_controls_24h.svg

   Compared to the 10h timepoint, both the later timepoints have slightly 
   better fold changes and much more normal traces.  I'm still a little bit 
   suspicious that the weird traces at the 10h timepoint were somehow flukes, 
   but in any case is seems like 10 is not enough for this strain.

   There doesn't seems to be any significant difference between the 17h and 24h 
   timepoints.  24h is usually more convenient, so I'll probably stick with 
   that for FACS.  However, I think I'll dilute my cells slightly more, to keep 
   them from being at stationary phase for too long.  The doubling time for 
   this strain seems to be about 3h, so 24h is about 8 doublings.  If I 
   inoculate 4 μL rather than 10 μL at the beginning of the experiment, I 
   should reach stationary phase right at 24h.
   
   .. figure:: 20170720_venus_controls_24h_event_rate.svg

   The tet populations (purple) are still growing 2x--3x more slowly than the 
   others.  Their traces look weird too, so I'll have to take another look at 
   how people use tetracycline with yeast in the literature, and maybe do a 
   titration.

References
==========
.. [Marcus13] Marcus and Raulet. A simple and effective method for 
   differentiating GFP and YFP by flow cytometry using the violet laser.  
   Cytometry A (2013) 83(11): 973−974.

