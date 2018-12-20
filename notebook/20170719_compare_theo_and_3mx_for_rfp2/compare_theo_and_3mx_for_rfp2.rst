*****************************
Compare theo and 3mx for rfp2
*****************************

James collected data for every design and every spacer with water, caff, theo, 
and 3mx.  This was a lot of work, but the some of the data doesn't look right.  
Specifically, the forward designs with the 3mx aptamer still respond 2x-3x to 
theophylline, although the 3mx aptamer is not supposed to bind theophylline at 
all.  I'm repeating the experiment just to make sure this is right.

I want to limit the number of reactions I do, to better ensure that I do 
everything right.  If James made a mistake, it would've been because he was 
trying to do so many reactions at once.  I'm going to start by doing just the 
rfp2 designs.  That means 20 reactions: 5 constructs times 4 ligands each.  If 
that's still too many, maybe I can drop `rxb 11,1` (which worked well in James' 
data) and `mhf 37` (which I'm not planning to include in the paper at the 
moment) to bring the total down to 12 reactions.

Preparing the media
===================
For 20 reactions, I need 10 mL 2x media, or five 2 mL aliquots.  I thawed six, 
just to be safe.  I need 5 mL of media (plus a little extra to be safe) with 
each ligand.  Six aliquots of 2x media is enough for 24 mL 1x media, or 6 mL 
per ligand, so I want between 5 mL and 6 mL of each.  I'll aim for 5.4 mL, 
because that will work out to give me nice round numbers.

All of the ligands are 30 mM, and I want them all to be 1 mM in the end.  That 
means 180 μL ligand per reaction:

======== ===== =========
Reagent   Conc    Volume
======== ===== =========
EZCCA       2x    2.7 mL
ligand   30 mM    180 μL
water          to 5.4 mL
======== ===== =========

James had his old solutions on his bench, but they had all crystallized a bit 
and I was uneasy about redissolving them.  My big concern was 3mx, which 
requires a little bit of NaOH to dissolve.  I probably would've had to add more 
NaOH to redissolve it.  But there was already a lot of NaOH in it (≈70 μL of 
10N NaOH), and I was worried about that affecting the results since I don't 
usually put NaOH in the "apo" reactions.

I decided to remake all of the ligand stocks and to add the same amount of NaOH 
(roughly) to all of them.  The exact quantities differed based on the exact 
amounts of ligand I weighed, but for each stock I used about 30 mg ligand, 5.5 
mL water, and 40 μL 10N NaOH.  All the ligands dissolved, although not 
immediately (theophylline was a little faster than the other two).  I stored 
all the ligand stocks in Falcon polypropylene tubes because they're resistance 
to degradation by NaOH, unlike glass.

Protocol
========
.. literalinclude:: 20170719_crispri_assay.txt

I repeated the above protocol on:

- Jul 19, 2017
- Jul 20, 2017

.. figure:: 20170719_rfp2_3mx_ligand_matrix.svg

These data look the same as James'.  I still can't explain for the 3mx aptamer 
responds to theo in the context of the forward design, but I'm willing to 
accept that it does in fact respond.


