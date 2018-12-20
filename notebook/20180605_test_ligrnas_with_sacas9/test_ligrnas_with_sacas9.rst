************************
Test ligRNAs with saCas9
************************

We were asked by reviewers to test the ligRNAs in the context of a Cas9 from a 
different species.  After reading some literature [Nakade2017]_, I settled on 
Staphylococcus aureus Cas9 (saCas9) as the most promising candidate.  CpfI is 
another popular Cas9 alternative, but its gRNA doesn't have the same stems as 
spCas9 (in fact it only has one 5-bp stem, which may correspond to the lower 
stem), so it's guide doesn't have a TRACR region.  (That said, Cpf1 may have 
been a better candidate for this aptamer-regulation strategy from the start...)

Methods
=======

Pick spacers
------------
Wildtype saCas9 has a NNGRRT PAM (R: G/A).  Kleinstiver2015_ used directed 
evolution to isolate a triple-mutant that supposedly has a NNNRRT PAM, although 
it still favors NNGRRT (and disfavors NNTRRT).  Since I was able to find 
wildtype PAMs near the beginning of both fluorophores (see below), I didn't 
think it was necessary to use the evolved construct.

CRISPRi repression is most efficient if the guide is complementary to the 
coding strand (meaning it would have the same sequence as the template strand).  
The PAM is on the template strand, just 3' of the spacer.  I always need to 
think through this, so here's an example::

   coding:   5'-AYYCNN ttttttttttttttttttttt-3'
   template: 3'-TRRGNN aaaaaaaaaaaaaaaaaaaaa-5'

Here the PAM in NNGRRT and the spacer is aaaaa...  For saCas9, the spacer is 21 
bp long (22 and 23 bp also perform well, ≤20 bp do not).  The coding strand 
usually appears on top, so the spacer and the PAM usually appear reverse 
complemented.

I searched for all occurrences of NNGRRT in the first 300 nt of the template 
strand of our chromosomally integrated sfGFP and mRFP genes.  The 300 nt limit 
was arbitrary; I just didn't want to test too many sequences.  I recorded the 
21 nucleotides 5' of each PAM as a spacer.  There is a PAM in the RBS, but I 
didn't record a spacer for it since such a spacer would target both 
fluorophores (they have the same RBS and start codon).  The spacers I chose are 
listed below:

=====  =====================
Name   Sequence
=====  =====================
sa/g1  AACATCACCATCTAATTCAAC
sa/g2  GTAGTGCAAATAAATTTAAGG
sa/g3  TCCAGTAGTGCAAATAAATTT
sa/g4  AAAGCATTGAACACCATAGGT
sa/g5  AGTCATGCCGTTTCATGTGAT
sa/r1  GGTAACTTTCAGTTTAGCGGT
sa/r2  ACCGTACTGGAACTGCGGGGA
sa/r3  TCAGGTAGTCCGGGATGTCAG
sa/r4  GAAGGACAGTTTCAGGTAGTC
=====  =====================

None of these spacers is predicted to interact strongly with the aptamer.  
Below are the predictions for mhf/30.  The predictions for rxb/11/1 are 
similar, but I didn't include them here because predicted ΔG doesn't correlate 
with success very strongly for rxb/11/1::

    $ cd notebook/20170329_test_multiple_spacers
    $ for x in {g1,g2,g3,g4,g5,r1,r2,r3,r4}; do echo $x; python3.6 predict_spacer_quality.py $x 'mhf 30' -s sa; echo; done 
    g1
    Spacer: AACAUCACCAUCUAAUUCAAC
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -2.7

    g2
    Spacer: GUAGUGCAAAUAAAUUUAAGG
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -4.2

    g3
    Spacer: UCCAGUAGUGCAAAUAAAUUU
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -4.3

    g4
    Spacer: AAAGCAUUGAACACCAUAGGU
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -7.3

    g5
    Spacer: AGUCAUGCCGUUUCAUGUGAU
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -11.6

    r1
    Spacer: GGUAACUUUCAGUUUAGCGGU
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -12.4

    r2
    Spacer: ACCGUACUGGAACUGCGGGGA
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -11.3

    r3
    Spacer: UCAGGUAGUCCGGGAUGUCAG
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -9.6

    r4
    Spacer: GAAGGACAGUUUCAGGUAGUC
    Insert: GCCGAUACCAGCCGAAAGGCCCUUGGCAGCGAC
    ΔG:     -9.6

Transplant ligRNAs
------------------
The sgRNA scaffold is slightly different between S. pyogenes and S. aureus, so 
I had to think about how I wanted to "transplant" the aptamer motifs from one 
scaffold to the other.  I decided to create two scaffolds: "sa" and "sap".  The 
first (mnemonic: "S. aureus") keeps as much of the S. aureus scaffold as 
possible.  The second (mnemonic: "S. aureus/pyogenes") keeps the nexus from S.  
pyogenes, since the nexus plays an important role in both rxb/11/1 and mhf/30 
work::

    $ sgrna_sensor sa/rxb/11/1 sap/rxb/11/1 sa/mhf/30 sap/mhf/30
    GUUUUAGUACUCUGGAAACAGAAUCUACUAAAACAAGGUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUACCGUGUUUAUCUCGUCAACUUGUUGGCGAGAUUUUUUUU
    GUUUUAGUACUCUGGAAACAGAAUCUACUAAAACAAGUGGGAUACCAGCCGAAAGGCCCUUGGCAGCCUACGUGUUUAUCUCGUCAACUUGUUGGCGAGAUUUUUUUU
    GUUUUAGUACUCUGGAAACAGAAUCUACUAAAACAAGGCGUGUCGCCGUAUACGCCGAUACCAGCCGAAAGGCCCUUGGCAGCGACUUUUUUU
    GUUUUAGUACUCUGGAAACAGAAUCUACUAAAACAAGGGUGUCCCGUAUACGCCGAUACCAGCCGAAAGGCCCUUGGCAGCGACUUUUUUU

Design primers
--------------
I ordered plasmid #70703 from Addgene.  This plasmid contains saCas9 and the 
saCas9 sgRNA.  I'm planning to use Gibson assembly to clone both into the 
plasmids I've been using for this project.  It's notable that the saCas9 gene 
is codon-optimized for human expression.  There was no bacteria-optimized 
saCas9 available on Addgene.  However, plasmid #70703 is a bacterial expression 
vector and was used in a bacterial directed evolution assay, so I have reason 
to believe it will express fine.  It's also notable that plasmid #70703 
contains an NLS and a 3xFLAG tag.  Neither of these should be necessary for me, 
but I decided not to make any changes to a construct that worked for the 
depositors.

I designed Gibson primers using the NEBuilder tool.  For the sgRNA assembly, I 
added the sa/g1 spacer in the primers.  I also designed primers to install all 
the remaining spacers in the sgRNA plasmid, and to create the negative control.  
Download a spreadsheet of the primers:

:download:`primers.xlsx`

Cloning spacers
---------------
2018/06/11:

- Streak the stab from Addgene (70703) on a fresh LB+Chlor plate.  Grow 
  overnight.

2018/06/12:

- Pick a colony (10:00) and grow in 5 mL LB+Chlor.

- Miniprep.  Yield: 83.8 ng/μL p70703.

2018/06/13:

- Decide to do 50 µL PCR to have enough material to gel purify.

- Use a 2:00 extension: Q5 is 20-30 s/kb, and my biggest amplicon was 3.6kb.  2 
  min is a bit on the long side, but I like being conservative w.r.t. extension 
  time.  I did all the reactions in one strip of tubes, so the sgRNA 
  amplication (only 0.9 kb) had a way-too-long extension time.  But it seemed 
  to work fine.

.. literalinclude:: 20180613_pcr_cloning.txt

2018/06/14:

- Gel purification:

  .. figure:: 20180614_gel_purify_sacas9_parts.png
     :width: 300 px

     Lanes from left to right: (1) Linearized pBLO1 (2) saCas9 from p70703 (3) 
     GeneRuler 1kb ladder (4) Linearized pBLO2 (5) sgRNA from p70703 (6) 
     GeneRuler 100 bp ladder. 

  I'm not sure what the high MW band for the sgRNA PCR is, maybe an artifact of 
  having too long of an extension time.

- Gibson assemblies

  .. literalinclude:: 20180614_gibson_assembly_sgrna.txt

  .. literalinclude:: 20180614_gibson_assembly_sacas9.txt

2018/06/15:

- Got a good number of colonies for both assemblies.  Slightly more for the 
  sgRNA one.

- Pick 3 colonies of each, send for sequencing.

saCas9
~~~~~~
2018/06/16:

- All three colonies had mixed peaks in the region where the assembly happened, 
  but clean (and correct) peaks before and after.  Are multiple plasmids 
  getting into each cell?  I'm not totally sure what happened.

- I'm going to pick 8 more colonies and see how they look.  If I don't have any 
  luck with those, I'll have to start optimizing the PCR.

sgRNA
~~~~~
2018/06/16:

- All three colonies had the right sequence.

- Miniprep

.. literalinclude:: 20180616_pcr_cloning.txt

2018/06/17:

- Didn't get any colonies.

2018/06/18:

- Run inverse PCR products on an 1% agarose gel.

.. note::

   The problem is that p70703 has a different Sa sgRNA sequence than the one I 
   copied down.  More specifically, it has an extended upper stem.  So the PCR 
   primers I ordered have a big mismatch in the middle.  I might be able to get 
   them to work, but I'd definitely need to use a lower annealing temperature. 

   The question is: which scaffold do I want to use?  The truncated scaffold is 
   from Ran2015_, which I believe was the first time saCas9 was used (I could 
   be mistaken about that, though).  Kleinstiver2015_ used the extended 
   scaffold, and I got my plasmid from them.  The upper stem of the extended 
   scaffold is longer by 4 base pairs, but is still not full length.

   Looking back at Ran2015_, they actually compared a number of upper stem 
   lengths (including the length that Kleinstiver2015_ ended up using) and 
   found that there's had the best editing efficiency.  I'm also inclined to 
   favor a short upper stem after a recent discussion with Tanja, where she 
   pointed out that a shorter stem might be less likely to interfere with 
   things (the context for that was rationalizing why the ligRNAs didn't work 
   in mammalian cells, though).  Interestingly, I found another saCas9 plasmid 
   from the Joung lab (earlier, I think) that had the truncated sgRNA (p65770).  

   Kleinstiver2015_ mention in their methods section that they changed the 
   length of the Sa sgRNA, but they don't explain why.  For their experiments 
   in bacteria, they used the extended scaffold for their selection assays and 
   the truncated one for their site-depletion assays.  I can't see any reason 
   why these assays would require different sgRNA scaffolds.  I half-suspect 
   that they just extended the stem just assuming it would be better, since the 
   optimized Sp sgRNAs do have extended stems, but didn't know that Ran2015_ 
   had already tried that optimization.  In any case, both seemed to work.

   I'm going to use the truncated scaffold moving forward.  It probably doesn't 
   make a difference, but there's some evidence that it works a bit better.  
   It's also the cheaper route, since I'll only have to order one set of 
   primers:

      KLEIN_TO_RAN_TM59_FOR	GAAacagaatctactaaaacaaggca
      KLEIN_TO_RAN_TM59_REV	cagagtactaaaacgttgaattagat

Test spacers
------------
2018/07/25:

- Make overnight cultures for all nine spacers (g1--g5, r1--r4).

- Start day cultures:

  - Prepare 10 mL LB + Carb + Chlor + aTc:

    - 10 mL LB
    - 10 µL Carb
    - 10 µL Chlor
    - 100 µL aTc

  - Inoculate 1 mL cultures with 4 µL overnight.

- Grow at 37°C for 8h.

The constructs did not grow well (i.e. the media pretty much looked clear, but 
I didn't measure OD).  I did flow cytometry anyways, and ended up with the 
following cell counts:

====  =====
Well  Count
====  =====
A02    1227
A04    2011
A06    2234
A08    1039
A10    2275
B02    1114
B02    1114
B04    6258
B06    3413
B08    1889
A02    1227
====  =====

I see pretty good repression for every spacer, but the very slow growth makes 
me hesitant to draw any conclusions.

.. figure:: 20180725_sadcas9_spacer_test.svg

2018/07/26:

I repeated the experiment from yesterday, but I grew the day cultures in EZ 
media that I prepared, aliquoted, and froze yesterday.  The cultures again did 
not grow well (with the exception of r2), and I did not bother to run flow 
cytometry.

2018/07/31:

I repeated the experiment from last week, but in an effort the get the cells to 
grow better, I grew both the overnights and the day cultures in EZ media.  The 
growth phenotype was interesting.  The g4 and g5 overnights did not grow, so 
instead of starting new day cultures, I left the overnights in the incubator.  
By the end of the day, they were very dense.  The g3 day culture did not grow 
well, so I simply added more of it to the plate for flow cytometry (2.5 µL 
instead of 0.5 µL).

Frankly, the growth phenotype seems stochastic.  If I had to guess, I'd 
attribute it to toxicity from sadCas9.  But I don't know how to confirm this, 
or what I'd do about it if I did.  Perhaps I could try reducing the 
concentration of aTc to 1x.  

.. figure:: 20180731_sadcas9_spacer_test.svg

- This time, the cell distributions were highly multi-modal.  g1, r1, and r3 
  were not so bad, but I expect that this is also a stochastic effect relating 
  to the poor growth (in part since all the constructs was mostly unimodal last 
  week).

- Regardless, I think it's reasonable to start constructing ligRNAs for g1 and 
  r1.

.. figure:: 20180731_sadcas9_spacer_test_gfp.svg

.. figure:: 20180731_sadcas9_spacer_test_rfp.svg

Test lower inducer concentrations
---------------------------------
Since my sadCas9 overnight cultures have seemed to grow well (except when I 
grew the overnights in EZ media), I'm suspicious that the poor growth I'm 
observing is due to the induction of sadCas9 by aTc.  Furthermore, since my 
uninduced overnight cultures have been either very red or very green, it 
doesn't seem that a lot of Cas9 expression is necessary for good repression.  

I'm also using extremely high concentrations of aTc.  `According to 
OpenWetWare`__, half-maximal induction is achieved at 42 ng/mL and the 
recommended 1x concentration is 100 ng/mL.  I've instead been using 1000 ng/mL, 
mostly following Qi2013_, who used 1 µM aTc (468 ng/mL) in their time-course 
experiments and 2 µM aTc (936 ng/mL) in their flow cytometry and 
β-galactosidase assays.  However, Qi2013_ didn't show an aTc titration, so I 
don't know to what extent they were just blasting dCas9.

__ https://openwetware.org/wiki/aTc

Vigouroux2018_ did an interesting study looking at different ways to get 
fractional CRISPRi repression, and for part of that they did try titrating aTc 
from 100 ng/mL down to 2 ng/mL in 6 steps.  Unfortunately they used a slightly 
different system (with dCas9 integrated rather than expressed off a plasmid), 
so their results aren't completely transferable to my system.  But they 
observed full repression at 100 ng/mL and 25 ng/mL, decreasing to about 60% 
repression at 10 ng/mL.  Since I have many more copies of dCas9 (by virtue of 
it being on a plasmid), it's very possible that I could use even less inducer 
than this.

I'm going to setup a plate reader experiment to test titrating aTc from 1000 
ng/mL to 1 ng/mL in 9 steps.  I'm also simultaneously going to setup a flow 
cytometry experiment with 1000 ng/mL aTc, 100 ng/mL aTc, and no aTc.  

.. note:: See binder for specific protocols.

Plate reader:

- The aTc toxicity is a strong effect that persists to even the lowest levels 
  of inducer tested (1 ng/mL, which according to Vigouroux2018_ is not enough 
  to stimulate any repression with spCas9).

- The spacer has no effect on toxicity, although since all of the spacers 
  repress similarly, this isn't surprising.

.. figure:: 20180802_sadcas9_atc_toxicity_od600.png 

Flow cytometry:

- Only the cells without aTc grew.  Both the 100 ng/mL and 1000 ng/mL cultures 
  looked equally thin (although I did not measure OD).  This is consistent with 
  the plate reader data.

- I got good repression even without inducer, though, so I can just simply not 
  use inducer.

- In terms of which target sequence is the best to move forward with, the 
  results I got from this experiment agree qualitatively with the results I got 
  from the 7/25 experiment:

  - g2 and g3 seem like the best GFP spacers.
  - r3 seems like the best RFP spacer.  r1 also seems good.

.. figure:: 20180802_sadcas9_atc_toxicity.svg

Test ligRNAs
------------
I decided to use g2, g3, r1, and r3 for a first round of experiments.  This is 
based both on how well they repressed with the controls, and their predicted ΔG 
for binding with the aptamer.

I prepared media without any aTc, based on the results from my experiments with 
inducer concentrations.  Specifically, my apo media was LB + Carb + Chlor while 
my holo media was LB + Carb + Chlor + theophylline.

.. literalinclude:: 20180820_crispri_assay.txt

Results
=======
The negative controls weren't transplanted effectively, which is to say that 
they retained pretty good repression.  To compensate for this, I changed the 
negative control, e.g. for the GFP constructs, to use the GFP channel for the 
RFP off constructs (and vice versa for the RFP constructs).  This required that 
I normalize each cell event by SSC rather than the non-targeted fluorescent 
channel, but the data looks good and is completely interpretable.

I see no evidence of the designed sensitivity to theophylline for any of the 
spacers.  I believe that I tested enough spacers (all predicted to be 
ligRNA-compatible) that I can rule out poor spacers as the cause of the lack of 
activity.  Note that the ligRNA⁺ constructs have, if anything, a small amount 
of activity in the wrong direction.  The strongest signal is sa/r3/rxb/11/1, at 
about 1.5x, but the other rxb constructs have either no signal or switch in the 
wrong direction (sa/r1).

.. figure:: 20180817_sadcas9_test_ligrnas.svg

If I wanted to get ligRNAs that worked with saCas9, I'd have to repeat the 
screens.  Given that I do not see any value in having these constructs, I'm not 
going to further pursue this direction.

An interesting sidenote is that CRISPRi works well with sadCas9, but only if 
it's not induced.  This may be a noteworthy result, since I wasn't able to find 
any examples of saCas9 being used for CRISPRi in bacteria (although I didn't 
look very hard).  It's also interesting to me that the expression level needs 
to be turned down all the way, although I still get the same level of 
repression in the end.  Is sadCas9 just a much more potent binder, and that 
potent binding causes toxicity at higher expression levels?  If so, would there 
be a way to get even tighter repression with saCas9?  Clearly simply increasing 
expression is toxic, but maybe if the cause of the toxicity could be 
determined, it could be alleviated.

References
==========
.. [Nakade2017] :doi:`10.1080/21655979.2017.1282018`
.. [Kleinstiver2015] :doi:`10.1038/nbt.3404`
.. [Ran2015] :doi:`10.1038/nature14299`
.. [Qi2013] :doi:`10.1016/j.cell.2013.02.022`
.. [Vigouroux2018] :doi:`10.15252/msb.20177899`


