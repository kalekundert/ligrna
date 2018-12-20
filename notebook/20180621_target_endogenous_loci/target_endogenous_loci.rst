**********************
Target endogenous loci
**********************

The reviewers asked if we could use ligRNAs to target endogenous loci.  After 
discussing with the Carol Gross lab, we decided that there were two ways to 
approach this: targeting LacZ and targeting auxotrophic genes.  Tanja is 
generally opposed to assays that involve survival, since cells can confound 
them in unexpected ways, so we're going to begin by targeting lacZ.

A basic overview of the lac operon is as follows:  The operon itself consists 
of lacZ (β-galactosidase), lacY (β-galactoside permease), and lacA 
(β-galactoside transacetylase).  We can assay the catalytic activity of lacZ 
using a variety of colorimetric assays.  lacY is required to transport both 
lactose and IPTG into the cell [Hansen1997]_.  lacA can attach acetyl groups to 
lactose, but I don't know what the biological purpose of that is.  In the 
absence of lactose (or IPTG), lacI (the lac repressor) binds to the operon and 
prevents its transcription.  

Transcriptional activation of the lac operon also depends on the cya and crp 
genes.  cya encodes for an adenylate cyclase, which produces cAMP.  crp encodes 
for CRP, which recruits RNA polymerase to the lac operon in the presence of 
cAMP.  So both cya and crp expression are required for the lac operon to be 
expressed.  

There are three regulator binding sites in the lac operon, termed A, P, and O.  
The CRP-cAMP complex binds the A-site and recruits the polymerase to bind the 
P-site.  lacI binds the O-site, but note that targeting the O-site with 
CRISPR/Cas9 inhibits expression of the operon, presumably because Cas9 is 
blocking the polymerase similarly to how lacI would.

Methods
=======

Tips
----
It took me a long time to optimize this assay, and here are the things I 
learned in the process:

- The cells need to be in late log phase (OD 0.5−1.0 with a 1 cm path length, 
  no more than OD 0.5 in the plate) before starting the reaction.  Earlier than 
  this, the signal for conditions with repressed lacZ is nearly within the 
  noise of the blank.  I never tried using cells later than this (e.g. in 
  stationary phase), but according to OpenWetWare that would make the results 
  less accurate (although the assay would still work).

- It's essential to measure A420 at several different timepoints, then to 
  adjust the baseline such that the resulting trace goes through the origin.  
  Specifically, I fit a line to the A420 data, then plug the slope into the 
  Miller unit equation.  Without this normalization, the activity will vary 
  with time.

- 1 mM IPTG seems pretty standard.  I tried to optimize this, but that was 
  before I had the assay really working and the data weren't interpretable.

- I don't think I should use EZ media for this assay, because glucose represses 
  the lac operon.  I haven't tested this, though.

Ordering
--------
Qi2013_ targeted all of the aforementioned genes and sites: lacI, lacZ, lacY, 
lacA, cya, crp, A, P, and O.  The largest effects were observed for lacI, lacZ, 
A, P, and O.  Note that targeting lacI results in the gain of β-galactosidase 
activity in the absence of IPTG, while targeting the other sites results in the 
loss of activity in the presence of IPTG.  Below are the sequence for these 
guides::

   lacI     5’-GCUGGCCUGGUUCACCACGC-3’
   lacZ     5’-UUGGGAAGGGCGAUCGGUGC-3’
   lacY     5’-GUAGCCAAAUCGGGAAAAAC-3’
   lacA     5’-CGGUAAGCCUUCGCACAUAU-3’
   crp      5’-ACAAGAACCAUUCGAGAGUC-3’
   cya      5’-GUCAAGCAGCAGUAUAUGCU-3’
   A site   5’-UGUGAGUUAGCUCACUCAUU-3’
   P site   5’-CUUCCGGCUCGUAUGUUGUG-3
   O site   5’-AUGUUGUGUGGAAUUGUGAG-3’

My plan is to test both control and both ligRNAs (4 total sgRNAs) with all 5 of 
these spacers.  I ordered primers for the aforementioned sites with the largest 
effects to clone into my sgRNA plasmid::

   LA_TM60_FOR	TTAGCTCACTCATTgtttcagagctatgctggaa
   LA_TM58_REV	CTCACAactagtattatacctaggactgagctag
   LI_TM60_FOR	CTGGTTCACCACGCgtttcagagctatgctggaa
   LI_TM58_REV	GCCAGCactagtattatacctaggactgagctag
   LO_TM60_FOR	TGTGGAATTGTGAGgtttcagagctatgctggaa
   LO_TM58_REV	CAACATactagtattatacctaggactgagctag
   LP_TM60_FOR	GCTCGTATGTTGTGgtttcagagctatgctggaa
   LP_TM58_REV	CGGAAGactagtattatacctaggactgagctag
   LZ_TM60_FOR	AGGGCGATCGGTGCgtttcagagctatgctggaa
   LZ_TM58_REV	TCCCAAactagtattatacctaggactgagctag
   
There are commercial kits available to measure β-galactosidase activity.  
Qi2013_ used the "yeast β-galactosidase assay kit (Pierce #75768, now Thermo)".  
Eames2012_ used the "β-Galactosidase Assay Kit (Stratagene)".  I looked at both 
kits and decided to use the Pierce one.  It just looks higher-throughput 
because it includes a detergent to lyse the cells, while the Stratagene kit 
requires a sonication step.  I'm going to have 4 sgRNA scaffolds × 5 spacers × 
with and without theophylline × with and without IPTG (maybe?) = 40, maybe 80 
conditions, so I'll really want to do this is a 96-well format.  Ziyue showed 
that sonication is the gold-standard for lysing cells, but I'm guessing the 
detergent will work fine for lacZ if a commercial kit is based on it.  I was 
also a little worried about the kit having "yeast" in the name, but the product 
page for the lysis reagent (Y-PER) indicates that it should work for bacteria 
too.

Here is the manual for the Thermo kit: :download:`MAN0011388_Yeast_BetaGalactosidase_Asy_UG.pdf`

Cloning
-------
2018/06/26:

- Setup a separate PCR master mix for each scaffold:

  .. literalinclude:: 20180626_pcr_cloning.txt

2018/06/27:

- Got a good number of colonies for all 20 transformations.  I'm anticipating a 
  high success rate, so I going to pick one colony for each to grow overnight 
  and miniprep, rather than doing colony PCR.

Optimize Assay
--------------

Optimize [IPTG]
~~~~~~~~~~~~~~~
2018/07/12:

Concentrations of IPTG between 0.1 mM and 4.0 mM seem to be common for protein 
expression.  Qi2013_ just used 1 mM IPTG, added at the same time as the ATC.  
It would probably be fine to use the 1 mM IPTG like Qi et al, but I want 
to get some experience with this assay and titrating IPTG seems like a good way 
to do that.  

The Thermo kit has "stopped" and "non-stopped" protocols.  I think Qi2013_ used 
the "non-stopped" protocol because they mention in their methods that they used 
100 µL of culture for each experiment.  The "non-stopped" protocol calls for 
100 µL culture, while the "stopped" protocol only calls for 70 µL.  Also, if 
I'm not sure how long the reaction will take, the "non-stopped" protocol is 
probably better because I can just take periodic measurements and figure out 
where the linear range is after the fact.

I think I can use clear plates for this assay.  White walls are helpful for 
luminescent assays (e.g. the sample is producing light, but usually not very 
much, so reflective walls amplify the signal), while black walls are helpful 
for fluorescent assays (by absorbing some of the incident light).  For 
colorimetric assays, think clear walls are fine.  If I were worried about 
crosstalk between wells, I might want opaque walls.

I gave some thought to how to measure OD600.  I need to measure OD600 as a 
normalization for enzyme activity.  Unfortunately, OD600 measurements in plate 
readers are not very accurate because they don't have a defined path length.  
The path length depends on the volume of media, the shape of the meniscus, and 
the position of the beam within the well.  However, for my experiments, I don't 
need absolute OD600 measurements.  I'm interested in the level of lacZ activity 
relative to my controls, so it will be enough to know the relative ODs.  Even 
though I won't know the path length for any well, I will be able to compare 
well because they should all have nearly the same path length: I put the same 
volume in each well, each well should have the same surface tension, and the 
beam should be focused the same for the whole plate.  

Below is the protocol I used, with the following caveats:

- I added 8 µL of IPTG (rather than 4 µL) in wells A1 and B1, because in the 
  protocol I forgot to account for the fact that there are 2 mL of media in 
  those wells.

- I put 1 mL of media in A4 as a blank well, and filled all the extra wells 
  with water to encourage everything to grow the same.

- I attempted to take time points at 5h40 and 7h15, but the data for the 5h40 
  timepoint was uninterpretable because I didn't get rid of te bubbles in the 
  wells (I was hoping that they'd pop on their own).

- Also for the 5h40 timepoint, well B2 didn't get enough WS reagent.  This was 
  due to an unnoticed repeater pipet error.  In the future, it'd be better to 
  use a multichannel pipet.

- It's hard not to get bubbles, because the cell lysis reagent is a detergent.  
  For the future, I experimented with a few techniques:
  
  - Reverse pipeting: Helps, but doesn't allow me to mix by pipeting.  Maybe I 
    could add a mix step to the spectrophotometer to compensate, though.

  - Misting 70% EtOH over the plate: Works pretty well, but gets some EtOH in 
    each well.  This might be good once I know how long to run the reaction 
    for, and am not measuring multiple timepoints anymore.  As it is, misting 
    the plate in the beginning increases the chances that it could affect the 
    reaction.

  - Gently squeezing EtOH vapor: This is a similar idea to misting, but using a 
    suqeeze bottle instead of a mister.  The idea is to squeeze gently enough 
    that no liquid comes out, but some vapor does.  This also pops bottles 
    pretty well, but I find that I mess up and accidentally squirt some EtOH in 
    the reaction too often for comfort.

  - Hot needle: I didn't try this, but it might be a good way to get rid of 
    straggler bubbles after one or two EtOH mistings.  Basically I'd get a 
    syringe needle and briefly heat it in a bunsen burner.

.. literalinclude:: 20180713_optimize_iptg.txt

This data isn't really interpretable, but I decided to go forward with 1 mM 
because that's what Qi et al used.

Optimize Time
~~~~~~~~~~~~~
2018/07/13:

- 2h timepoint: I reverse-pipeted the reagents, but did nothing to mix.

- 3h timepoint: I tried reverse-pipeting-to-mix, but of course I ended up with 
  some volume left in all the tips.  I decided that it would be 

- I haven't finished plotting this data yet, but they seem to be strongly 
  affected by the OD of the initial culture.  I want to repeat this experiment, 
  but with diluting the cells to (roughly) the same OD each time.

.. literalinclude:: 20180713_optimize_time.txt

Tube vs. Plate
~~~~~~~~~~~~~~
2018/07/16:

I found that `this OpenWetWare`__ page had some really useful information on 
the β-galactosidase assay.  Some of the key take-aways:

__ https://openwetware.org/wiki/Beta-Galactosidase_Assay_(A_better_Miller)

- "Miller recommends a culture with OD600 = 0.28 to 0.70. However, he claims 
  that overnight cultures can also be used but that exponentially growing cells 
  give more precise assays [1]."

- To account for cell debris, you can measure A₅₅₀ and subtract 1.75*A₅₅₀ from 
  A₄₂₀.  1.75×A₅₅₀ approximates the amount of scattering at A₄₂₀ that is 
  attributable to the cell debris.  Alternatively, you can centrifuge the 
  reaction for 5-10 minutes at max speed to pellet any debris, but this 
  precludes doing the assay in 96-well plate format. 

- "In his book, Dr. Miller explains that this formula yields approximately 1 
  Miller Unit for uninduced E. coli (low β-Gal production) and approximately 
  1000 units for a fully induced culture (grown on lactose or IPTG).  In my 
  experience, cultures of MG1655 induced with 1 mM IPTG in log phase have 
  1500-1800 Miller units."

- "Miller recommends that the OD420nm reading should ideally be 0.6-0.9.  I got 
  reproducible data when the yellow color was just detectable before adding the 
  stop solution up to about the color of LB broth before stopping. Remember, 
  you need the substrate to saturate the enzyme during the course of the 
  reaction, so don't let them go too far."

  - Note: The Thermo kit claims that A420 values from 0.02–1.0 are 
    within the linear range of the assay.

- It might make sense to make the reaction buffers myself.  

  - It would probably be cheaper, although I might not do the assay enough for 
    that to really matter.

  - I probably wouldn't have to worry about freezing and thawing that one 
    buffer.  I think I have to do that because it contains β-mercaptoethanol 
    (BME), but it I made the buffer myself I could make it fresh and keep it at 
    4°C for a few days.  

  - I could make a control without ONPG, to control for the absorbance of cell 
    debris at A420.

Today, I want to try the following things:

- Induced and uninduced cultures.  This will let me know if I'm in the right 
  range for Miller units.

- Plate (with A550 correction) and tube (with pelleting).  This will let me 
  know how accurate the correction is, and if I can really do the assay in a 
  96-well format.

- Time course with positive and negative control sgRNAs: This will let me know 
  how long it takes to get maximal CRISPRi signal.

- Undiluted cultures and cultures diluted to approximately OD660=0.04.  I'd 
  like to be able to normalize away the effect of the cell debris, but for the 
  purpose of the time course and determining how long it takes to get the 
  maximal differential CRISPRi signal, it would be best to compare reactions 
  with similar ODs.

  I chose 0.04 because that's a value obtainable by the early timepoints.  I'm 
  a little worried that the reaction never really gets into the linear regime 
  with that few cells (at least when lacZ is being repressed), 

- To do a kinetic measurement with tubes, I'll need to mix the tubes, maybe 
  incubate for 5 min, pellet, transfer to plate, then start kinetic run.  That 
  should be fine, the first 10 minutes always look kinda screwy anyways (maybe 
  as the cell debris settles or something).  But it means I will need to really 
  keep track of how long it takes to get the plate  in the spectrophotmeter.

  I'll be measuring A550 at every timepoint anyways, so I should see if more 
  debris keep crashing out.  But I don't think it will, based on how the 
  reading stay pretty constant after about 15 minutes.

- 2 mL cultures, just so I won't run out, and each sample I take affects the 
  volume less.  That means inoculating with 8 µL of overnight culture.

- Given that I'm trying to measure cells with fairly different levels of 
  activity, maybe the stopped protocol would be better?  Maybe.  If it's a 
  problem, when I'm doing my real experiments, it would probably be easier to 
  do the kinetic reads, rather than monitoring each reaction independently.  
  Although, kinetic reads do limit me to one plate at a time...

.. literalinclude:: 20180713_optimize_time.txt

- The on cultures didn't grow noticeably in the 6h experiment.  I'm not sure 
  what happened.  I'm pretty sure I did inoculate those cultures, and they did 
  grow after I left them in the incubator overnight.  

- I forgot to measure OD660 for the 4h timepoint, so I can't calculate Miller 
  units for that timepoint.

- I collected data such that I could stitch together longer time-sourses for 
  the earlier datapoints, but I didn't actually bother to do that in the 
  analysis script.

- I'm really uneasy that the β-galactosidase activity is so variable with 
  respect to time.  Some possible explanations:

  - I'm running out of reagent.  Not likely because I start measuring as soon 
    as faint yellow appears, and the kit should provide an excess of reagent.

  - Maybe the frequent reads are photo-bleaching the yellow product.

  - Maybe the spectrophotometer isn't measuring time accurately, e.g. maybe it 
    waits 1 minute between reads, but doesn't account for the time the reads 
    themselves take?  This seems absurd, but I'm suspicious because I've 
    sometimes checked back on it and found that it had completed fewer reads 
    than I was expecting.  I haven't checked carefully, though.

- Pelleting the reaction seems to reduce the enzyme activity significantly.  I 
  guess a lot of the enzyme is either insoluble, or caught up in the insoluble 
  fraction.  For accurate measurements, I probably need to quench the reaction, 
  then pellet it, then measure absorbance.

.. figure:: plots/20180716_optimize_time.svg

    Black: +IPTG.  Grey: −IPTG.  Solid lines: plate reactions.  Dotted lines: 
    tube reactions.  Note that centrifuging seems to remove a significant 
    amount of enzyme, so only the first timepoint is truly meaningful for these 
    traces.  

- The 1.75×A550 normalization didn't work.  With that normalization, all my 
  reactions had intercepts far from 0, some above, some below.  I decided to 
  instead normalize by fitting a line through the data and subtracting the 
  intercept.  This worked well, except when the absorbance data itself was 
  kinda curved.  Maybe an exponential fit would be better.

- It's very strange to me that the *rate* of some of the reactions seem to be 
  increasing linearly over time.  I could understand a decrease in rate, but 
  what could be causing an *increase*?  Maybe debris settling?  MAybe I didn't 
  mix the cells well enough, so the lysis reaction is continuing?

- Induced cells are supposed to have around 1000 Miller units, while uninduced 
  cells are supposed to have around 1 Miller unit.  I'm not even close to these 
  figures in this experiment, but I don't know why.

2018/07/17:

Today, I want to make another attempt to see if I can get enzyme activity 
values that aren't time-dependent.  I'm also testing my designs, because I've 
gotten kinda impatient.

- I abandoned this experiment because there was a weird precipitate in media 
  and the cells din't grow very well.  I wonder if I've left the EZ media at 
  4°C too long?  Teknova says EZ media should be stable at 4°C for two weeks, 
  but should not be frozen.  I kinda want to use LB, just to not have to deal 
  with this.  Alternatively, I could make fresh EZ media +/- IPTG...

2018/07/18:

Repeat same experiment as yesterday, but:

- Use LB instead of EZ media:

  - 19 mL LB
  - 20 µL carbenicillin
  - 20 µL chloramphenicol
  - 200 µL anhydrotetracycline
  - 20 µL 1M IPTG
  - Vortex to mix
  - Split into 2 8.7 mL portions
  - To one portion add 300 µL 30 mM theophylline (9.1 mg theophylline, 1683.5 
    µL water), to the other portion add 300 µL water.  In hindsight, it might 
    have been a little better to dissolve the theophylline in LB.

- Setup the day cultures in duplicate.  I only made one overnight culture for 
  each strain, so this isn't really a full biological duplicate.  My main goal 
  here is to build trust with the assay, and a duplicate might help with that.

- After 4h, the cells were at OD600=0.1293 (1 cm path length).  In retrospect, 
  I should've waited until they were at OD600=0.5–1.0.  (This is what the 
  Thermo protocol recommends).   One of my problems right now is that the signal 
  I get from my repressed samples is within the noise of the blank, so I don't 
  know their activity and can't calculate fold changes.  To counter this, I 
  need more enzyme, which means more cells.

.. literalinclude:: 20180717_tube_vs_plate.txt

- There isn't much variation within the technical replicates, so I don't think  
  it will be necessary to do three technical replicates for each biological 
  replicate.

- It's clear that both ligRNAs have signal.  The dynamic range for ligRNA⁻ is 
  small, but I think adding more cells might help (the signal in this 
  experiment was pretty much at the lowest detectable values).  Having more 
  divisions 

- I'm not sure why the plate measurements seem so time-dependent here.  The 
  rate does decrease with time, so maybe there's some bleaching or significant 
  decrease in substrate going on.  I'm also kinda surprised by how 
  time-independent the tube measurements are.  I mean, that's how they should 
  be, but I've not had any luck with that up to now.

  .. update:: 2018/07/22
    
      The time dependence is probably due to the intercept of the A420 traces not 
      being 0.  I didn't correct for that in this script.

.. figure:: plots/20180717_tube_vs_plate.svg
    
    Grey: controls.  Navy: ligRNA⁻.  Teal: ligRNA⁺.  Darker shades: tube 
    reactions.  Lighter shades: plate reactions.  Error bars are standard 
    deviation of two technical replicates.

2018/07/21:

I repeated this experiment with just the controls to focus on the question of 
whether tubes and plates produce comparable data.  I also sought to grow the 
cells to OD600 0.5–1.0, as mentioned above.

- I took about 6h30 for the cells to reach OD600≈0.8.

.. literalinclude:: 20180722_tube_vs_plate.txt

- The results from the plate seem pretty comparable to those from the tubes.  
  The difference is that the tubes give about 2x more signal across the board.  
  This may be a consequence of the quenching step (someone on OpenWetWare 
  mentioned that quenching, which is done by reducing the pH, can increase the 
  absorbance of ONP).  The increase is pretty similar for both controls (≈2.1x 
  for lz/on and ≈1.7x for lz/off), so I don't think it'll be signficant when 
  calculating fold changes.

  This is good news, because it means I can do the assay in high throughput and 
  that I can use a kinetic protocol to measure rates.

  One thing I'm worried about is sufficiently mixing the cells after adding 
  Y-PER.  I'm suspicious that this is the reason I saw reactions where A420 
  curved upwards in some of my earlier experiments.  It was easy to mix the 
  cells well in tubes, but in plates I'll need to pipet-to-mix, which will 
  introduce bubbles.  I can see two ways to deal with this:

  - Pop all the bubbles by hand.

  - Make more than I need (e.g. 250 µL) and transfer 200 µL to a clean plate.  
    A small thing here is that I'll have a different path length for the OD 
    and A420 measurements, but that won't matter if I'm calculating fold 
    changes.

- In the future, I don't think I need the debris control.  What was really 
  important was getting the A420 to go through the origin.  Since the debris 
  control appears to be pretty constant over time, the intercept adjustment is 
  a better way to do this.

  It might make sense to have a blank, e.g. Y-PER + WS + media, to control for 
  auto-hydrolyzation of ONPG.  I don't really think this is an important 
  factor, but it's also pretty easy to control for.

.. figure:: plots/20180721_tube_vs_plate.svg

    Blue, green: lz/on, lz/off.  Darker shades, lighter shades: tubes, plates.  
    Top panels: Normalized A420 for each timepoint.  Middle panels: A420 of the 
    debris control for each timepoint.  This is one component of the 
    normalization in the top panels.  Bottom panel: β-galactosidase activity 
    (in Miller units) for each reaction, at each timepoint.

Dress rehearsal
~~~~~~~~~~~~~~~
2018/07/24:

Before testing all constructs I prepared, I wanted to do the assay once as if I 
were doing the high-throughput assay, but just with the lz constructs.  My goal 
was just to get used to the assay and to make sure that everything still works 
when I'm not doing the hybrid tube/plate assay.

.. literalinclude:: 20180725_beta_gal_assay.txt

- The fold changes in this assay are comparable to those I get from the flow 
  cytometry assay, which is nice. 

- In this assay, ligRNA⁻ achieves nearly full repression while ligRNA⁺ achieves 
  nearly full expression.  In the flow cytometry assay, both dynamic ranges 
  were more intermediate.

- The data for the holo positive control is funky, in that the rate of the 
  reaction curves up right at the end.  I don't know what caused this, but I 
  decided to fit only the linear region leading up to it.

.. figure:: plots/20180724_dress_rehersal_fits.svg

    A420 vs time for each sgRNA.  Data points are shown with '+' and '-'. 
    symbols.  The former are included in the linear fits, while the latter are 
    excluded.  The fits themselves are shown with lines.  The black points and 
    lines represent the without-ligand condition, which the colored points and 
    lines represent the with-ligand condition (1 mM).

.. figure:: plots/20180724_dress_rehersal_miller.svg

    Rates, OD600s, culture volumes, and β-galactosidase activities (Miller 
    Units) calculated for each sgRNA, with and without ligand.  The activities 
    are just the rates divided by the OD600s and the volumes.

.. figure:: plots/20180724_dress_rehersal_fold.svg

    The fold change in β-galactosidase activity for each sgRNA.

Lyse before ONPG
~~~~~~~~~~~~~~~~
2018/08/02:

In an effort to make the raw data more linear, I'm going to try letting the 
lysis reaction incubate for 1h before adding the ONPG reagent.  I'm also going 
to test the effect of adding cold vs. room temperature ONPG.

- In addition to the ONPG reactions described below, I also setup two sets of 
  reactions where I added the lysis reagent before the ONPG reagent.

  - Aliquot 60 µL of ONPG buffer into two sets of 10 PCR strip-tubes.  Incubate 
    one strip at room temperature and the other at 4°C.

  - Pour the Y-PER into a reagent reservoir, and add 50 µL to the two 
    aforementioned sets of reactions, using a multi-channel pipet.  Mix well.
    
  - Incubate at room temperature for 1h.

  - Add 50 µL of ONPG reagent (room temperature to one set of reactions, 4°C to 
    the other).

  - Measure A420

.. literalinclude:: 20180802_beta_gal_assay.txt

The upward curve at the beginning of the reaction does seem to be caused by the 
progression of the lysis reaction.  It wasn't so bad this time, but you can see 
that most of the concurrent reactions curve upwards for the first 30 min or so.  
In contrast, the pre-lysed reactions are linear from the very start.  I'm going 
to keep doing the pre-lysis, even though I can correct for it by picking the 
linear region, because (i) it makes the raw data look more convincing, (ii) I 
don't have to worry about traces that never really look linear, and (iii) it's 
not hard.

Interestingly, pre-lysing didn't eliminate an upwards curve towards the end of 
the trace.  The remaining effect is pretty consistent: about 0.05 A420 upwards 
creep over a 2h time course.  That's negligible for the more active constructs, 
but pretty significant for the others.  I wonder if this could be debris 
settling.  (Note: I went to look at an old debris control, but for all those 
experiments I was just collecting 1-3 timepoints, not full time courses, so I 
wouldn't be able to see this effect.)  If that were the case, I could either run blank wells (which could 
be expensive depending on how many I decide to do), or I could content myself 
with using the just analyzing the earliest data points.

Alternatively, the lysis reaction could *still* be not complete.  In this case, 
though, I'd expect the magnitude of the effect to be bigger for the more active 
constructs.  Unfortunately we can't tell for the most active ones, because they 
eventually become ONPG-limited, but the effect is much smaller (relatively 
speaking) for rxb/11/1 apo than for on.

Theophylline also seems to be having a consistent effect on the controls.  I'm 
pretty sure this is not due to differential CRISPRi activity, because my 
controls were always completely insensitive to theophylline in flow.  There is 
a slight differential growth phenotype (in this experiment, at least), but it's 
much smaller than the magnitude of the effect, and should be controlled for 
anyways.  Maybe I should also try washing the cells before starting the 
reactions, in case theophylline is speeding up lacZ somehow?  It's also 
possible that the reaction is just sensitive to small perturbations when 
there's not much enzyme activity.

.. figure:: plots/20180802_pre_lyse_merged_fits.svg

    Top row ("concurrent"): The lysis and ONPG reagents were added at the same 
    time.  Middle row ("pre-lyse 22°C"): The lysis reaction was started 1h 
    before the ONPG reagent was added.  The ONPG reagent was at room 
    temperature.  Bottom row ("pre-lyse 4°C"):  As previous, but the ONPG 
    reagent was at 4°C.  The gap in the "concurrent" traces is from when I had 
    to take the plate out of the reader to start the pre-lysed reactions (which 
    up to that point had just been lysing).  The linear fit fails for A3 
    because the data trends downward, which confuses the method the analysis 
    script uses to pick to first and last data points.

.. figure:: plots/20180802_pre_lyse_merged_miller.svg

Wash theophylline
~~~~~~~~~~~~~~~~~
The last big problem with this assay is that theophylline has a large effect on 
the controls, especially the positive control.  I hypothesized that his might 
be because the theophylline in the media affects the enzyme, so I decided to 
add a wash step (pellet cells, then resuspend in PBS) before starting the 
reaction to see if this would help.

At the same time, I tested two strategies to mitigate the upwards curve I see 
in a lot of the reactions.  The first was to run a debris control (Y-PER, but 
no ONPG) the see if the effect could be explained by cellular debris settling.  
The second was to use a black plate, to rule out interference (somehow) from 
neighboring cells. 

- Washing did more to counter-act the upward curvature than the debris control 
  did, although the debris control also helped.  For example, the unwashed 
  "on" reactions (apo and holo) see almost no benefit from blanking (top figure 
  to bottom figure), but significant benefit from washing (top panels to bottom 
  panels).  Interestingly, the holo washed "on" sample also sees significant 
  benefit from the debris control, as do the unwashed "rxb/11/1" samples.

  - I can't understand how washing would help with the upwards curvature.  That 
    implies that there's something about the media itself that increases A420 
    over time, but the effect is negligible for the media alone (i.e. the blank 
    well).  I wonder if I'd see an effect for media that cells grew in, but 
    without cells, e.g. the supernatant from the wash.

  - When I did the wash, I was a little worried because the pellets were so 
    small.  (Of course, this is a natural consequence of pelleting a small 
    volume of not-very-thick cells.)  More specifically, I was worried that I'd 
    lose a significant number of cells in the washing (although in this case, 
    the ODs with and without washing were very similar).  OD60 is taken into 
    account by the Miller equation, so this shouldn't be a problem, but it 
    still worries me.

  - I made a mistake when setting up the debris control: I added 50 µL ONPG to 
    the reactions, but forgot to add a corresponding amount of liquid (e.g. 
    water) to the debris controls.  So the wells had significantly different 
    volumes.  In a perfect world that wouldn't matter, but in the real world it 
    might have.

- Washing did not help at all with the sensitivity of the controls to 
  theophylline.  That implies that the theophylline is not directly 
  interfering with the β-galactosidase assay.

- The holo controls consistently have both more enzymatic activity and a higher 
  OD.  I wonder if the differential activity is a consequence of being in 
  mid-log phase, where small differences in cellular health might have an 
  inflated effect on the amount of lacZ that's been expressed (e.g. healthier 
  cells start producing lacZ earlier, and end up with more lacZ per cell when I 
  start the reactions).  I could try growing the cells for 8h like I normally 
  do for flow, which might allow the cells to get closer to stationary phase.  
  I could also try doing the assay on saturated overnight cultures (which is 
  supposed to work).  I also want to try diluting the cells to the same OD 
  before running the experiment, just to confirm that the OD normalization 
  isn't fucked up somehow.
  
.. figure:: plots/20180804_test_washing_unblanked_fits.svg

.. figure:: plots/20180804_test_washing_blanked_fits.svg

Growth Time
~~~~~~~~~~~
I thought that more saturated cultures might give more consistent results 
between the controls, as small difference in growth and induction timing would 
have greater opportunity to even out.  So I setup apo and holo reactions for 
the controls, and measured β-galactosidase activity at 4 different time-points: 
6h, 8h, 10h, and overnight (≈24h).  In every case, I diluted each sample to 
about OD600=0.2 (plate reader path length).

- The result I got from this assay were not consistent with the results I've 
  gotten in the past.  First, the 6h timepoint showed nearly identical levels 
  of activity for the apo and holo cultures.  Second, in all the other 
  timepoints, the apo reaction was more active (in the past it was the holo 
  reaction that was almost always more active).

- I did two things differently than usual with the 6h reaction.  First, I 
  accidentally added 100 µL of Y-PER instead of 50 µL.  Second, I diluted the 
  cells to approximately the same OD.  I don't think the latter caused the 
  improved consistency, because I diluted the 8h, 10, and o/n samples in the 
  same way.  I also don't think the extra Y-PER made a difference.  If it did, 
  it would either be due to better lysing the cells or by diluting the ONPG.  
  Both possible, but unlikely in my view.

.. figure:: plots/20180807_test_growth_time_merged_fits.svg

.. figure:: plots/20180807_test_growth_time_merged_miller.svg

.. figure:: plots/20180807_test_growth_time_merged_fold.svg

Mix vs No Mix
~~~~~~~~~~~~~
Because mixing the wells is very difficult to do without introducing bubbles, I 
tried setting up the overnight reaction from above both with and without 
mixing, to see if I could get away without it.

- The bumpy trace for `apo on` shows why I have to mix.  Presumably, the rate 
  of the reaction is changing as the reagents mix.  This isn't always a 
  problem, but I don't want to be throwing away any fraction of my data.

.. figure:: plots/20180807_mix_vs_no_mix_fits.svg


β-galactosidase assay
---------------------
2018/07/26:

- The ODs were too high, and as a result the ONPG became limiting and the 
  traces were very non-linear.  This surprised me, since I grew the cells for 
  exactly 6h30 (just as in the dress rehearsal).  In the future, will dilute 
  the cells to below OD 0.5 if necessary.

- The dynamic range is narrow: The lacZ-expressing controls are at about 500 
  Miller units (rather than 1000).  I don't know what caused this.

- The `lo` cells did not grow well.  I don't know if this is because they were on 
  the bottom of a stack of three blocks.  Next time, I'm going to use the flat 
  plate-holder thing.

- The ligRNAs didn't work very well this time.  I want to chalk that up to the 
  high ODs, but 

.. figure:: plots/20180726_target_lac_fits.svg
    
.. figure:: plots/20180726_target_lac_miller.svg

2018/07/31:

- I diluted all the samples except `lo` by 25% (e.g. 75 µL culture + 25 µL 
  fresh LB) to get all the ODs below 0.5 (some were still slightly above).  I 
  chose OD=0.5 because samples with ODs lower than that didn't seem to plateau 
  in the 7/26 experiment.  In retrospect, maybe I should've aimed for OD=0.15, 
  since that's what I got good results with in the dress rehearsal.

- It bothers me that the early data points curve upwards.  I think this happens 
  because the lysis reaction takes a long time to finish.  To test this, I I 
  want to run a reaction where I add just the lysis reagent, incubate for 1h, 
  then add the ONPG reagent.
  
  Another possible explanation is that the plate is slowly warming up.  
  According to the data, the temperature in the plate reader fluctuates between 
  24.5°C and 24.7°C.  My protocol doesn't specify a temperature, so presumably 
  this is just the natural temperature in the plate reader.  Room temperature 
  in the lab is slightly cooler than that (22.5°C today), but I don't think 
  that's significant.  What may be significant is the temperature of the 
  samples, which are 2:1:1 mixtures of culture (37°C), Y-PER (23°C), and ONPG 
  (4°C), all left at room temperature for varying amounts of time.  I can't say 
  what the final temperature of the mixture is, but if it's significantly 
  cooler than room temperature, then it will slowly warm up during the 
  experiment.  Maybe I can test this in the same experiment as above, by adding 
  either cold or RT ONPG.

- The controls were very theophylline-sensitive in this assay.  Given that I'm 
  pretty confident that neither growth nor anything intrinsic about the 
  controls is theophylline-sensitive, this is probably a sign that something 
  about the assay isn't robust.  But I don't know what that would be.
  
.. figure:: plots/20180731_target_lac_fits.svg
    
.. figure:: plots/20180731_target_lac_miller.svg

2018/08/09:

I didn't include the `lo` constructs in the experiment, because they had a 
severe growth defect for some reason.  I'm not planning to look into it, 
though, since I think I have enough data as it is.

.. literalinclude:: 20180820_beta_gal_assay.txt

.. figure:: plots/20180809_target_lac_fits.svg

.. figure:: plots/20180809_target_lac_miller.svg

Results
=======
The ligRNAs are certainly still functional targeting the lac operon, but the 
effect seems weaker than it did with the fluorescent proteins.  The signal in 
both assays is *supposed* to be directly proportional to the amount of protein 
expressed, but it's probably not worth reading too much into the difference 
between two different assays.

I'm surprised that rxb/11/1 didn't do so well, since it's normally the more 
robust ligRNA.  It did better in some of my earlier experiments, but those 
experiments also exhibited significant responses to theophylline in the 
controls (due to differences in OD, I believe), so I think the data presented 
below is correct.

Note that I'm not presenting any data for the `lo` spacer, since those 
constructs consistently grew very slowly.  I didn't investigate the cause of 
the growth defect, but my first guess would be something to do with the aTc 
(since the overnights seemed to grow fine, similar to 
:expt:`20180605_test_ligrnas_with_sacas9`).

.. figure:: plots/20180809_target_lac_fold.svg

References
==========
.. [Hansen1997] :doi:`10.1007/s002849900320`
.. [Eames2012] :doi:`10.1126/science.1219083`
.. [Qi2013] :doi:`10.1016/j.cell.2013.02.022`

