***********************************
Measure ligRNA induction time-scale
***********************************

We are interested to know how fast ligRNAs can effect a change in the level of 
gene expression in response to the addition or removal of the ligand.  From 
previous qPCR experiments (done by Fitzy) measuring the level of sfGFP 
expression, we know the response to ligand is complete after 30 min.  The goal 
of this experiment is accurately determine time scale of the response by 
measuring mRNA levels 1, 2, 4, 8, 16, and 32 min after adding and removing 
ligand.

Taking measurements with this level of time resolution will be technically 
challenging.  Harvesting RNA requires pelleting enough cells to get adequate 
yield, removing the supernatant, then incubating the pellet in TRIzol.  These 
steps needs to be completed as fast as possible in order for the experiment to 
work.  The swinging-bucket centrifuge is to slow, so I have to use a table-top 
one.  That limits me to 1 mL of culture, so I need to start from relatively 
thick cultures.  I will also need to practice to ensure that I can pellet the 
cells and begin the TRIzol incubation in less than a minute.

Notes
=====
- Possible controls:

  - No-template control (NTC, no-cDNA).  Possibly redundant

  - No-reverse-transcriptase control (NRT, no-RT): tests for contamination by 
    gDNA.

  - MG1655 without GFP or RFP (no-GFP).  This controls against non-specific 
    amplification (would corroborate melting curves).  Possibly makes the 
    no-template control redundant.

  - Primers that amplify untranscribed regions of genomic DNA, to ensure that 
    RNA extraction was clean.  Possibly redundant with no-reverse-transcriptase 
    control.

  - Positive control (gfp/off)

  - Negative control (gfp/on)

  .. update:: 2018/12/19

      I ended up doing only the NTC, the NRT, and the MG1655−GFP controls.
   
- How many samples do I plan to run?  This might affect my decision about 
  whether to use 96- or 384-well plates:

  - 7 timepoints: 0, 1, 2, 4, 8, 16, and 32 min.  Might only decide to do 6.

  - 4 constructs: on, off, rxb/11/1, mhf/30

  - 2 ligand conditions: apo, holo (i.e. removing, adding ligand respectively).

  - 2 primer sets: 16S rRNA, sfGFP

  - 3 technical replicates

  This adds up to 336 wells for 56 different conditions.  The 384-well plate 
  would let me do everything in one run, which eliminates concerns about 
  comparing across samples.

  Note that this doesn't include any of the aforementioned controls.  But I 
  could do those on a separate plate.

  .. update:: 2018/12/19

     I ended up organizing the experiment rather differently than I had planned 
     above:
      
     - 10 timepoints (0, 2:00, 4:20, 7:00, 10:00, 13:20, 17:00, 21:00, 25:20, 
       30:00) (each timepoint is an additional 0:20 longer than the previous).  

     - 2 constructs: rxb/11/1 and mhf/30 only.  I decided that for this 
       experiment, apo→apo and holo→holo with the ligRNAs themselves was a 
       better control than using the on/off sgRNAs.
       
     - 4 ligand conditions: apo→apo, apo→holo, holo→apo, holo→holo

     - 3 controls: no-cDNA, no-RT, no-GFP

     With the same number of primer pairs and technical replicates as planned 
     above (and considering that there are only two ligand conditions for the 
     0:00 timepoint), this adds up to 474 qPCR reactions.  I did them on two 
     384-well plates: one for rxb/11/1, and one for mhf/30.

- Does TRIzol kill cells?  I needed to be sure that it does, because the first 
  step of the RNA extraction protocol is a 5 min incubation in TRIzol (before 
  chloroform is added), and I won't be able to get the time resolution I want 
  if the cells are alive during that incubation.  Fortunately, from `wikipedia 
  <https://en.wikipedia.org/wiki/Guanidinium_thiocyanate>`_:

   Guanidinium thiocyanate is also used to lyse cells and virus particles in 
   RNA and DNA extractions, where its function, in addition to its lysing 
   action, is to prevent activity of RNase enzymes and DNase enzymes by 
   denaturing them. These enzymes would otherwise damage the extract. 
  
- Reference gene primers: ihfB and rrsA (i.e. 16S rRNA) are the most commonly 
  used reference genes for bacteria.  Zhou2011_ points out that there might be 
  better choices, but I'm inclined to stick with what we've already been using.

- Reverse transcription:

  There are two primary kinds of reverse-transcriptase (RT): Avian 
  Myeloblastosis Virus (AMV) and Moloney Murine Leukemia Virus (MMLV) 
  [PromegaRT]_.

  - AMV: Has RNase H activity to degrade template as cDNA is transcribed.  This 
    precludes the synthesis of long cDNA strands, but is better for ensuring 
    that you get exactly 1 cDNA molecule for each RNA molecule.  Optimal AMV 
    activity is at a relatively high temperature (42–48°C) which can increase 
    the rate of RNA hydrolysis.  However, AMV is also better at 
    reverse-transcribing through secondary structure.
    
  - MMLV: Less RNase H activity, and the most popular variant contains a point 
    mutation that eliminates RNase H activity altogether.  Optimal reaction 
    temperature is 37°C.  MMLV is better for reverse transcribing long RNAs 
    (>5kb) with weak secondary structure.

  Superscript VILO (Invitrogen 11755050) is an engineered MMLV variant.  
  Probably it would've been better to use an AMV RT, since my transcripts are 
  short and the more guaranteed 1:1 ratio would be good, but I already know 
  that VILO one works fine, so I'll probably just stick with it.

- MIQE guidelines

  A set of recommendations to ensure high-quality qPCR data [Bustin2009]_.  See 
  also `<http://www.rdml.org/miqe.php>`_.  Review the attached checklist, and 
  make sure I follow its recommendations:

  - :download:`MIQE_checklist.xls`

- ROX normalization

  Only necessary for qPCR machines which use a single camera to image all the 
  wells at once, as the distance between the camera and the well varies across 
  the plate.  For the BioRad CFX machines, ROX is not necessary.  It can be 
  included, but is probably best not.

- ΔΔCt analysis

  For ΔΔCt analysis, it's important that the efficiencies of the test and 
  reference primer pairs be within 5%.  Normally a range of 90–110% is 
  considered acceptable, but since these primers will be compared with each 
  other, they need to be closer.

  - Pfaffl Method: Account for the difference in efficiency between the test 
    primers and the reference gene primers.

  - Vandesompele Method: Same as Pfaffl method, but allows more multiple 
    reference genes.  This is obviously more accurate, but also requires many 
    more control samples.
    
Methods
=======
Download the primers I used for this experiments:

:download:`primers.xlsx`

2018/10/26
----------
The qPCR experiment done by Fitzy shows that the reaction is complete in before 
the first timepoint (30 min).  Other interesting points:

- GFP expression seems to trend downward over time, for both the controls and 
  the ligRNAs.  I cannot think of any explanation for this phenomenon.

- It's noteworthy that even rxb/11/1 has completely responded to ligand in 30 
  min.  Our understanding is that Cas9 binds very tightly to DNA, and so it's 
  surprising that an active sgRNA/Cas9 complex can become inactive so quickly.

  I have to read more about what known about the kinetics of Cas9/DNA binding 
  to know how surprising this is really, though.

.. figure:: 20181026_gfp_timecourse_cmf.svg

2018/11/17
----------
- I only grew 9 mL of each day culture (and inoculated with only 36 µL of 
  overnight, accordingly).

- I wish I had done the incubations in a 37°C thermomixer.  When I was planning 
  the experiment, I was thinking mostly about the short timepoints, but for the 
  long timepoints, being at room temperature could definitely slow the kinetics 
  of mRNA transcription.

- I resuspended the RNA in 30 µL water in order to get concentrations around 
  600 ng/µL (otherwise I would be working with volumes too small to pipet in 
  the next step).

- I think I could next time just keep 400 µL of the TRIzol from each 
  extraction.  That would be a little easier, because I wouldn't be straining 
  to avoid the organic phase, and I would also get the same amount from each 
  sample (as it is, I get 500-600 µL depending on the sample) which might lead 
  to more consistent RNA yields (not that it really matters, because I dilute 
  the RNA anyways, but I figure that more consistency is always better) (and I 
  don't need to worry about yield for this experiment).

.. literalinclude:: 20181119_induce_and_trizol_fast.txt

Optimize qPCR parameters
~~~~~~~~~~~~~~~~~~~~~~~~
Before running qPCR on all 57 cDNA samples, I used the off/apo/0min cDNA to 
optimize my primer concentrations and melting temperature for qPCR:

More specifically, I tested 3 different concentrations of primers (50 nM, 300 
nM, and 900 nM) and a temperature gradient from 55.6°C to 65.6°C as recommended 
by the Power SYBR Green master mix manual (it had other recommendations that I 
didn't test, for the record):

:download:`power_sybr_green_manual.pdf`

- Prepare the primer dilutions.

  The primer stocks are 200 µM.  I first prepared a mix of 5 µM forward and 5 
  µM reverse primers for both the sfGFP ("gfp") and 16S rRNA ("16s") primers:

  - 38 µL water
  - 1 µL forward primer
  - 1 µL reverse primer

  Each of my qPCR reactions will be 8 µL and will contain 3 µL of primer mix 
  (as described the next step).  Therefore, for final primer concentrations of 
  900, 500, and 50 nM, I needed primer mixes that were 2400, 800, and 133.3 
  nM:
  
  2400 nM:
  - 26 µL water
  - 24 µL 5 µM primer mix
    
  800 nM:
  - 42 µL water
  - 8 µL 5 µM primer mix

  133.3 nM:
  - 48.67 µL water
  - 1.33 µL 5 µM primer mix

- Setup the qPCR reactions::

     ─────────────────────────
     Reagent     µL/rxn  µL/54
     ─────────────────────────
     master mix       4    216
     primer mix       3
     cDNA             1     54
     ─────────────────────────

  I setup each reaction without technical replicates.  I wanted to save 
  reagents, and I assumed that I would be able to see a trend between the 
  reactions at different temperatures and that that trend would serve to give 
  me sufficient confidence in the results.

- Run qPCR:

  Heat seal:

  - 167°C for 3s

  Thermocycler settings:

  - 95°C for 10 min
  - Repeat 40x:
    - 95°C for 15s
    - 55.6°C - 65.6°C for 1 min

  The specific temperatures for each row, as estimated by the thermocycler, 
  were as follows:

  - A: 65.5°C
  - C: 65.0°C
  - E: 63.9°C
  - G: 62.2°C
  - I: 60.0°C
  - K: 58.1°C
  - M: 56.6°C
  - O: 55.7°C

I looked for the combinations of primer concentration and melting temperature 
that gave the best amplification, i.e. the lowest Cq values:

- In general, 300 nM was the most efficient primer concentration.

- The 16s primers worked best at slightly cooler temperatures than the gfp 
  primers.  However, 60.0°C seemed like a pretty good compromise between the 
  two.

- I think the data would've been more consistent and less noisy if I had done 
  technical replicates.  It might also have helped to do larger reactions (e.g.  
  25 µL instead of 8 µL).  But overall I think the trends are apparent and the 
  results make sense.

:download:`20181122_optimize_tm_primer_conc_gfp_16s/report.pdf`

::

   $ ./optimize_tm_primer_conc.py

.. figure:: 20181122_optimize_tm_primer_conc_gfp_16s.svg

qPCR for the time-course
~~~~~~~~~~~~~~~~~~~~~~~~
- The data was noisy and a number of reactions failed.  I didn't bother going 
  through and marking the bad reactions as outliers, because I don't think the 
  data has what I want to see.  I think the problem is that (a) I did 8 µL 
  reactions, which meant that (b) I had to accurately pipet 1 µL of cDNA.  
  Making everything worse, (c) I added the cDNA before the PCR master mix, so I 
  had trouble ejecting all the cDNA and keeping it in the well.

  In the future, I should do 25 µL reactions and add the cDNA last.

- I'm pretty sure I didn't mess up the labels (a concern with such a big, 
  complicated plate), because the controls make sense and rxb/11/1 holo→apo 
  (the only reaction that seems to have a clear trend) goes in the right 
  direction.

:download:`20181122_ligrna_induction_timecourse/report.pdf`

::

   $ ./fit_half_life.py 20181122_ligrna_induction_timecourse.toml -o $.svg

.. figure:: 20181122_ligrna_induction_timecourse.svg

2018/11/24
----------
I didn't have enough reagents to repeat the whole experiment at 37°C, but I 
wanted to test at least one ligRNA to get a sense of whether 37°C would even be 
any different from room temperature:

- I accidentally stopped the 3 min reaction too early, so I got a 2 min 
  timepoint instead. 

- I resuspended the RNA in just 10 µL water, because the pellets looked small.  
  This was a good idea; my yields were 310±126 ng/µL, which in some cases was 
  just barely enough to get 1 µg in the RT reaction.

.. literalinclude:: 20181124_induce_and_trizol_practice.txt

The 0 min and 2 min timepoints were not really consistent with each other.  
This might be because I stopped the 0 min timepoints before I even started 
setting up the rest, so there were ~10 minutes really between the 0 min and 2 
min timepoints.  Next time, I think I'll try to do the 0 min timepoints 
immediately after starting all the other samples, to avoid this potential 
issue.

That said, the 0 min timepoint seems to fit better with the rest of the data 
(e.g. the 2 min timepoint looks like an outlier, see below).  Fortunately, the 
half life is about 5 min in either case, so perhaps it doesn't matter too much.

Note that I see a ~10x change in mRNA concentrations between the 0 min and 30 
min timepoints, which is in line with what we've seen in previous experiments.

:download:`20181124_practice_timecourse_mhf_30/report.pdf`

::

   $ ./fit_half_life.py 20181124_practice_timecourse_mhf_30.toml -o '$.svg'

.. figure:: 20181124_practice_timecourse_mhf_30.svg

   qPCR timecourse with all timepoints included.  Note that first points are 
   not fit very well.

::

   $ ./fit_half_life.py 20181124_practice_timecourse_mhf_30.toml -O -o '$_wo_2min.svg

.. figure:: 20181124_practice_timecourse_mhf_30_wo_2min.svg

   qPCR timecourse with the 2 min timepoint excluded.  Note the better fit.

2018/12/{01,03,13}
------------------
- Because I could only do a limited number of samples at once, I had to split 
  the experiment over two days.  I decided to do ligRNA+ on one day and ligRNA− 
  on the other, since I wouldn't be making comparisons between the tow ligRNAs.  

- On Tanja's advice, I using didn't collect data for the on/off control sgRNAs, 
  instead using the apo→apo and holo→holo conditions as controls.  I think this 
  was a good decision.  For this experiment, we already know that the ligRNAs 
  work, so we don't need a control to establish the maximum possible dynamic 
  range of CRISPRi.  However, we do need a control to separate the effects of 
  our handling the cells (which we do a lot of) from the effect of the ligand.

- Also on Tanja's advice, I stopped trying to fit the data to a model (e.g. an 
  exponential curve).  We just don't know enough to build a kinetic model, and 
  we don't need one for the conclusions we're trying to make.

- I had to repeat the qPCR for the ligRNA+ timecourse, because the 
  amplification curves were very inconsistent the first time.  I'm not sure 
  exactly what went wrong, because I thought I setup the reactions flawlessly.  
  I made the following changes the second time I ran the timecourse (which gave 
  excellent data):

   - I ordered new primers.  I did this because the 16S rRNA reactions were 
     much more consistent (although one still failed), so I thought the problem 
     might be with the sfGFP primers.

   - I ordered new qPCR master mix, because I was out.

   - I spun the plate right-side-up and upside-down 4 times (after 
     heat-sealing) to better mix the reactions.

   - I accidentally left the plate at room temperature for >2h before starting 
     the reactions, because the qPCR machine failed to start and I didn't 
     notice until I came back to get the results.

.. literalinclude:: 20181218_induce_and_trizol_fast.txt
.. literalinclude:: 20181218_reverse_transcribe_mhf.txt
.. literalinclude:: 20181218_reverse_transcribe_rxb.txt

Results
=======
- mRNA levels react to the addition of theophylline on a time-scale of 5-10 
  minutes.

- For both ligRNAs, turning GFP expression on is faster than turning it off.  
  This is not what we'd expect if Cas9 releasing from DNA was a very slow 
  process.  In fact, adding theophylline to ligRNA- seems to have the fastest 
  response of anything.

- I think we need to know more about the kinetics of mRNA expression and dCas9 
  binding to know whether this data is surprising or not.

::

   ./gfp_mrna_vs_time.py data/20181201_ligrna_timecourse.toml -H

.. figure:: 20181201_ligrna_timecourse.svg

   left plot: ligRNA+, right plot: ligRNA-, grey dashed line: apo->apo control, 
   grey solid line: holo->holo control, colored solid line: apo->holo 
   timecourse, black dashed line: holo->apo timecourse.  GFP mRNA levels are 
   relative to 16S rRNA levels.

References
==========
.. [Zhou2011] :doi:`10.1186/1471-2199-12-18`
.. [PromegaRT] https://www.promega.com/resources/pubhub/choosing-the-right-reverse-transcriptase/
.. [Bustin2009] :doi:`10.1373/clinchem.2008.112797`

