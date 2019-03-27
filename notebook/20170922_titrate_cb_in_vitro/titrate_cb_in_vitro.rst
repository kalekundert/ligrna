*********************
Titrate cb (in vitro)
*********************

I want to include an in vitro titration in the paper, but the gels I have are 
kinda smeary.  So my goal is to repeat the titration and do a better job of 
running the gel.

Methods
=======

Transcribe RNA --- Sep 22, 2017
-------------------------------
I made 30 μL aliquots, because I need 1.5 μL sgRNA/rxn, and I'm planning to do 
15 reactions (to have the same number of lanes as the other gel I want to show 
in figure 1).  That adds up to 22.5 μL, rounded to 30 μL to be safe.

.. literalinclude:: 20170922_transcribe_sgrna.txt

In vitro Cas9 cleavage --- Sep 23-25, 2017
------------------------------------------
I did a 14-step 2-fold serial dilution of theophylline for the titration:

- In the 1st well, put 50 μL 30 mM freshly prepared theo.  I'm not sure that it 
  was necessary to freshly prepare the theo, but I was having so much trouble 
  with this experiment that I wanted to eliminate any possible source of error.
- In the 2nd--14th wells, put 25 μL nuclease-free water
- Perform a serial dilution, transferring 25 μL at each step.
- In the 15th well, put 25 μL nuclease-free water

I used 25 μL for the serial dilution, even though the reactions only need 5 μL, 
because I was more confident in my ability to accurately pipet the larger 
volumes.

I used a new box of tips for the experiment, to decrease the likelihood of any 
dust somehow getting on the tips and contaminating things.  (I've been taking 
more and more precautions with RNA because I've been having so much trouble 
with degradation in my in vitro transcription reactions, and these precautions 
are carrying over to my Cas9 reactions.)

To get publication-quality results, I used a 140 mL 1% TAE/agarose/GelRed gel.  
I let the molten agarose cool for 5 min on a rocker before adding the GelRed 
and pouring the mixture into the cast (the purpose of this step is explained in 
the `Troubleshooting`_ section).  I cast the gel in the Owl Easycast B2 tray 
with the 1 mm thick 20-tooth comb.  I loaded 2 μL of ladder (GeneRuler 1kb, 
Thermo SM0312) and ran the gel at 85V for 90 min.

.. literalinclude:: 20171004_cas9_cleavage_assay.txt


Results
=======

.. figure:: 20171003_titrate_cb_new_rna.png

   Lanes 1,2: aavs/wt without and with theo.
   Lanes 3,4: aavs/dead without and with theo.
   Lanes 5-20: aavs/cb with titrated theo, starting at 10 mM and decreasing by 
   2x each step, no theo in the lane 20.

The EC50 is very inconsistent between all the replicates I performed.  My 
hypothesis is that the EC50 is just very sensitive to parameters that are hard 
to control, like the quality of the RNA, the age of the Cas9, and the exact 
quantity of DNA.  The EC50 for this titration is 1 mM, but I think I should 
present this data simply as evidence that the cleavage as ligand dependent and 
avoid interpreting the EC50.

.. figure:: find_apparent_kd.svg

   The fit is a 3-parameter logistic model: :math:`Y = Y_{\rm min} + 
   \frac{Y_{\rm max} - Y_{\rm min}}{1 + {\rm EC}_{50} / X}`

Troubleshooting
===============

Wrong comb --- Sep 23, 2017
---------------------------
I used the Owl EasyCast B2 tray with the 25-tooth comb, and ran the gel at 100V 
(4.5 V/com) for 70 min.

The titration looks really good, but the gel wouldn't look right next to figure 
1e: the comb is clearly different and the bands are smiling noticeably more.  

.. figure:: 20170923_titrate_cb.png

Bad gel --- Sep 25, 2017
------------------------
I looked back at the original image for figure 1e, and it's clear that I used a 
20-tooth comb for that gel.  The only 20-tooth comb we have is for the B2 tray, 
so at least I know that.  I decided to use the 1 mm side of the comb because 
its wells have a similar footprint to the 25-tooth wells (3.2 mm × 1.0 mm vs.  
2.0 mm × 1.5 mm).

To eliminate the smiling, I decided to post-stain the GelRed.  I used about 120 
mL of freshly prepared 3x GelRed and soaked the gel for 10 min.

.. figure:: 20170925_titrate_cb_morning.png

Cody pointed out to me that the smearing may have been caused by me pouring the 
molten agarose into the gel cast while it was still too hot.  I couldn't get a 
clear answer on the internet, but it stands to reason that the agarose might 
cool at different rates near the gel tray versus near the surface, and that 
these different rates of cooling could lead to heterogeneities in the gel.

In the interest of making a gel that looks like figure 1e, I'm also going to go 
back to putting the GelRed in the gel.  You can tell that I didn't used 
post-staining for figure 1e by looking at the ladders.  In figure 1e, the 
ladder bands are just slightly W-shaped.  In this gel, they're totally flat.  I 
think a combination of the wider wells and a lower voltage will give me a 
comparable gel.

Inconsistent brightness --- Sep 25--26, 2017
--------------------------------------------
I mixed 140 mL TAE with 1.40 g agarose, then microwaved the mixture for 2m30 to 
melt the agarose.  I then gently rocked the molten agarose at room temperature 
for 5 min.  I tried to monitor its temperature with the laser thermometer, but 
the readings it gave me were inconsistent, so I just stuck with the 5 min rule 
of thumb suggested to me by Anum and the internet.  After 5 min, I added 14 μL 
GelRed (10,000x in water), poured the agarose into the gel tray, and let it 
cool for 30 min.  Then I ran the gel at 85V for 90 min.

.. figure:: 20170925_titrate_cb_evening.png

The gel finally looks comparable to figure 1e, so I'm happy with all the gel 
parameters I had to work out.  However, it looks like I added too much DNA to 
the 8th and 10th cb reactions, and maybe not enough RNA to the 2nd.  The 
inconsistent band intensities really ruin the titration effect, so I have to 
repeat this reaction again.

I repeated this reaction being careful to check the tips for drops, but got the 
same inconsistencies again.

.. figure:: 20170926_titrate_cb.png

Poor titration --- Sep 30, 2017
-------------------------------
I think I resolved the inconsistent brightness issue (in this experiment and in 
several for the multiple spacer assay) by making sure to mix the DNA (just by 
flicking) after it thaws.  My hypothesis was that DNA was most concentrated 
wherever in the tube froze last, and that I just needed to be sure to mix 
anything that was frozen and thawed.

However, this titration doesn't look as good as they others have.  The 10 mM 
point is closer th 50/50 than 80/20, and the apparent Kd is ≈4x higher than 
before.  I don't think this is because I'm just adding more DNA now that the 
DNA is better mixed, because the titration still fades faster even when only 
looking at the 2kb band.  (Also, I think the DNA was well-mixed in the first 
experiment, and it looks good.)

As I see it, the problem is probably with either the RNA or the theophylline.  

.. figure:: 20170930_titrate_cb.png

Poor cleavage --- Oct 1--2, 2017
--------------------------------
I repeated the titration with freshly transcribed RNA and freshly prepared 
theophylline.  The transcription reaction worked better this time than it had 
previously, perhaps because I added RNase inhibitor to the reaction.

.. figure:: 20171001_transcribe_cb.png

Despite this, the titration still didn't look right.  This time, the problem 
was that the wt control only exhibited only ≈50% cleavage.  That considered, 
the titration is actually not bad.

.. figure:: 20171001_titrate_cb.png

I repeated this experiment in exactly the same way the next day, and got 
exactly the same result:

.. figure:: 20171002_titrate_cb.png

   At least my shitty results are reproducible...

It's plausible that the problem is with the RNA, because I made new RNA and got 
the same poor cleavage twice in a row, despite how good the gel looks.  I had 
the RNA in the 4°C for ≈1h before aliquoting and freezing it, and I was using 
RNase A at the same bench where I aliquoted the RNA.

But I'm also inclined to think there's a problem with the Cas9.  My old stock 
was almost out, so I ordered a new stock which I'll try in my next experiment.

Fresh Cas9 --- Oct 3, 2017
--------------------------
I repeated the experiment with fresh Cas9 from NEB that arrived today.  I also 
setup two titrations, one with the sgRNA from Sep 22 and one with the sgRNA 
from Oct 1.  My goal was to learn if the poor cleavage I saw in the last two 
experiments was due to the sgRNA (in which case I would still see poor 
cleavage) or the Cas9 (in which case I wouldn't).

.. figure:: 20171003_titrate_cb_old_rna.png

   Sep 22 sgRNA

.. figure:: 20171003_titrate_cb_new_rna.png

   Oct 1 sgRNA; It finally worked!

I didn't expect just one reaction to work well.  My interpretation of this is 
that the Se 22 sgRNA was always more degraded, although for some reason this 
wasn't a problem until it had been in the freezer for a week.  (The first four 
titrations with that RNA all spanned the full dynamic range, but the subsequent 
titrations never achieved full activation.  I used the original aliquots for 
the first four titrations, and I made new aliquots for the rest.  Perhaps I 
made a mistake diluting the sgRNAs the secon dtime, or perhaps the time the 
sgRNA wasa on the bench while I was diluting it was enough for it to be 
degraded by RNase contamination.  Freeze/thaw cycles can't explain the problem, 
because the fifth titration was still only thawed once.)

The Oct 1 sgRNA was better, but somehow on the same day my Cas9 stock went bad.  
It was getting low and it was a few months old, but I can't really think of 
anything I did to harm it.  I was handling proteinase K before setting up the 
Cas9 reactions, maybe I got some contamination?  Or maybe I just wasn't 
accurately pipetting 0.47 μL of Cas9 when I was doing one titration at a time, 
and what really helped was doing two titrations at once and upping the amount 
of Cas9 to an easier-to-pipet 0.94 μL.

