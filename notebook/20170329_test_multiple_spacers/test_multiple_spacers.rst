*********************
Test multiple spacers
*********************

I want to determine how broad the targeting range is for my sensors.  In other 
words, I want to know what fraction of spacers can be expected to work with my 
inducible guides.  

Planning
========

Which assay?
------------
I'm going to try to answer this question using my *in vitro* Cas9 cleavage 
assay.  

I can't use my *in vivo* CRISPRi assay because it's limited to to the spacer 
sequences present in sfGFP and mRFP, and only the first few work well enough 
with the controls to be worth using.  

I was hoping to be able to think of a way to do a really high throughput assay, 
but so far I haven't been able to.  I tried designing a construct that had a 
shared a randomized spacer sequence between the sgRNA and the 5' UTR of sfGFP, 
but it had only 2x repression for the AAVS spacer sequence (which works well in 
the *in vitro* cleavage assay).  I saw a paper that ordered DNA with the same 
random sequence present in two places (the sgRNA and the 5' UTR of a reporter 
protein), but I didn't figure out how they did that.  

So in lieu of something smarter, I'm just going to brute-force 20-40 spacers 
with my in vitro assay.

Which spacers?
--------------
The first thing I have to decide is which spacer sequences to use.  I can think 
of three ways to pick spacers:

1. Select spacers that have been validated in published experiments.  

2. Select spacers using published rules that try to predict how good spacers 
   will be.

3. Pick spacers randomly.  This is the easiest option, because I can just order 
   randomized primers and pick 20-40 different colonies; I won't need to keep 
   picking and sequencing colonies until I find one with the right sequence.

To decide between these three options, I looked for papers containing validated 
sgRNAs or describing rules to predict spacer quality.  I found two papers by 
one group that answer both inquiries well enough.  Doench14_ looks at CRISPR 
knockout data for 1841 targeting sites in 9 genes.  The data reveal the 
sequence preferences shown below:

.. figure:: doench_2014_fig_3a.svg
    :align: center

    I'm not sure how to interpret the y-axis.  Is 10⁻⁴ a lot?

The authors also publish a ranked list of all the sgRNA sequences they use, 
which I could use to pick validated target sequences: 

:download:`nbt.3026-S5.xlsx`

Doench16_ revises the rules from the 2014 paper using more data and more 
sophisticated machine learning.  However, they also show that the rules aren't 
as predictive for CRISPRi/a libraries as they are for knock-out libraries.  (In 
the paper they sell their method as being predictive for CRISPRi/a, but I don't 
think the data really supports this.)  This discrepancy makes me suspicious 
that the rules are in fact specific to gene knockout.

.. figure:: doench_2016_fig_4ef.svg
    :align: center

Granted, there are ways to explain this lack of predictive power for CRISPRi/a 
libraries.  Maybe where the sgRNA binds is more important for these 
experiments, and that effect overshadows how well the guides bind.  Still, 
based on this data, I'm not convinced that trying to adhere to these rules 
would be much better than picking sequences randomly.

I'm not sure how I would go about picking validated sequences.  I want good and 
bad sequences, but not sequences that don't work at all.  Should I somehow 
select for diverse sequences?  Diverse GC contents?  Do I need to worry about 
bias due to the relatively small number of genes in database?  I also need to 
keep in mind that my guides need to start with 2-3 G's in order for the T7 
polymerase to work efficiently.  Would it be better to limit myself to 
validated sequences that just happen to start with several G's?  Would that 
bias the sequences?  Or would it be better to just add 2-3 G's to the end of 
any sequence, even though those G's wouldn't complement anything?

I want to think about this more, but in the mean time I designed and ordered 
random primers.  I figured that I might as well get something started.  I made 
the first three nucleotides of each spacer ``GGG`` for T7 polymerase.  I also 
randomized the ``N`` in the ``NGG`` PAM, since Doench14_ suggested that that 
position can be important.  Here are the primers I designed::

    Number of oligos: 2
    Primer lengths: 24, 24

    Primer names (ready to copy into Elim form):
    SPACER_N17_TM_57_FOR
    SPACER_N17_TM_57_REV

    Primer sequences (ready to copy into Elim form):
    NNNNNNNNggtgacagaaaagccc
    NNNNNNNNNNcccactgtggggtg

I think the best way to frame the question of how to pick spacers is: I want to 
test as many spacers as possible.  If I'm too random, I'll probably end up 
testing spacers that don't work very well, which will reduce the amount of data 
I get.  If I'm too non-random, I'll probably end up testing spacers that aren't 
as diverse as they could be, which will also reduce the amount of data I get.  
I think Tanja's view has been that it's worth doing a quick pass to eliminate 
any spacers that look really bad.  My view has been that random spacers are 
significantly easier to make than designed ones.  I also worry that with the 
non-random strategies, you don't really know how many independent spacers you 
have in the end.  James also brought up the point that I don't want people to 
think I cherry-picked the spacers I end up testing, which is an argument for 
using a script to pick the spacers.

Ordering enzymes and kits
-------------------------
I'm going to order Cas9 from NEB for this experiment, because it's cheap 
(15¢/rxn) and I don't want to worry about having bad enzyme for such a big 
experiment.  The question is how much to order.  I'm planning to test 40 
spacers.  I have 5 guides (2 controls, 3 designs) to test with each spacer, 
with and without ligand, and I want to do everything in triplicate.  That 
means:

.. math::
    
    40 \times 5 \times 2 \times 3 = 1200\,\mathrm{rxns}

    1200\,\mathrm{rxns} \times 0.45\,\mathrm{pmol/rxn} = 540\,\mathrm{pmol}

Product number M0386T is 400 pmol.  That's not quite enough for the whole 
experiment, but it's still possible that I won't do the full experiment, and 
the next step up is way more than I need (2000 pmol).  So this seems like a 
good compromise.

========  ==========
Reagent   Product #
========  ==========
Cas9      NEB M0386T
XmnI      NEB R0194S
HiScribe  NEB E2040S
========  ==========

Miniprep vs. Miraprep
---------------------
I needed to decide whether to miniprep or miraprep the template DNA.  I plan to 
use each template with five guides (on, off, rxb/11/1, mhf/30, mhf/37), for 
three technical replicates.  That means I need to use each template for 15 
reactions.  Each reaction requires 1.5 μL of 30 nM DNA.  In total, then, I 
need:

.. math::

    15\,\mathrm{rxn} \times \frac{1.5\,\mathrm{μL}}{1\,\mathrm{rxn}} \times 
    \frac{30\,\mathrm{nmol}}{10^6\,\mathrm{μL}} \times \frac{4347\,\mathrm{bp} 
    \times 650\,\mathrm{ng/bp}}{1\,\mathrm{nmol}} = 1907\,\mathrm{ng}

That corresponds to 38 ng/μL for a 50 μL miniprep, which is easily achievable.  
So I can stick with regular minipreps.  I grew the cells up overnight in 3 mL 
LB in 24 well blocks.

PCR vs. restriction digest
--------------------------
After cloning the d1--d8 spacers into the on, off, rxb 11/1, mhf 30, and mhf 37 
constructs, I have two ways to produce linear DNA encoding the sgRNA: PCR and 
restriction digest.  I was originally planning to do PCR, but I realized that 
the sgRNA is naturally has an EcoRI site just upstream and a HindIII site just 
downstream.  I thought a restriction digest might be easier and more robust, 
but might not give as much DNA.  I ran a gel confirm that both methods produce 
DNA of the same size and to see which produced more DNA.

PCR protocol
------------
.. include:: 20170508_pcr.txt
    :literal:

Restriction digest protocol
---------------------------
.. include:: 20170510_digest_pblo_for_t7.txt
    :literal:

Results
-------
.. figure:: 20170510_d1_pcr_vs_digest.svg
    :width: 400px

This gel shows that restriction digest is a much more reliable approach.  Only 
one of the 5 PCR reactions produced the right product, and the others were 
rather heterogeneous.  Getting them all to work could require a prohibitive 
amount of optimization.  In contrast, the restriction digests just worked.  The 
products all seem to be a little bigger than I'd expect, but they're close 
enough that I'm not really suspicious of it.  You can also see that the five 
sensors run at speeds (controls > mhf > rxb) that correspond to their 
differences in size.

It does look like PCR produces more DNA, but I think the restriction digest 
produces enough.  Previously, I was using 10 ng gBlocks DNA.  This time, I put 
≈500 ng DNA into each restriction digest (although these miniprep yields were a 
little low; I'd expect to get closer to 1 μg in general).  My template is 150 
bp and the whole plasmid is 2.5 kb, so ultimately I should have 30 ng DNA:

.. math::

    \frac{500\,\mathrm{ng} \times 150\,\mathrm{bp}}{2500\,\mathrm{bp}} = 
    30\,\mathrm{ng\ DNA}
    
Since that's more than I've been using, I'm pretty sure I'll be fine.

The N17 spacers are biased
--------------------------
I sent 84 N17 colonies for sequencing, and I got 43 sequences back with spacers 
of the correct length (i.e. no insertions or deletions).

:download:`n17_spacers.tsv`

The spacers seemed to have a suspicious number of long runs of A's.  To 
quantify this suspicion, I calculated Pearson's χ² statistics for the 
distribution of nucleotides at each position with the null hypothesis is that 
the distributions are uniform.  I applied the Bonferroni correction to the 
resulting p-values to account for the fact that I'm testing multiple hypotheses 
(one for each position).  I also calculated these same statistics for spacers 
picked from a uniform distribution in python, as a sanity check:

.. figure:: n17_spacer_uniformity_test.svg

At the 99% confidence level, there are several positions that significantly 
deviate from a uniform distribution.  It's also clear the first half of the 
spacer is enriched for A, although the χ² test does not account for this kind 
of correlation.  Based on these observations, I can confidently conclude that 
the N17 spacers are not uniformly distributed.

This isn't really surprising, since I used inverse PCR to build these spacers 
and PCR is an exponential process.  I'm actually surprised that the bias seems 
to be towards A rather than C and G (or even A and T).  The long runs of A 
suggest that maybe it's advantageous for primers to be able to bind in multiple 
sites, but really I can't say what the mechanism underlying the bias is.

In any case, this bias definitively rules out using spacers cloned from 
degenerate primers for this assay.  Instead I'm going to randomly generate 
spacers in python and used the Doench16_ score function to prioritize them.

Designing Doench16_ primers
---------------------------
I'm planning to use the design rules in Doench16_ to filter my spacers.  I 
didn't look that hard for sgRNA design rules, so there may be others that I'm 
not considering.  I did consider Horlbeck16_ because Tanja specifically pointed 
it out to me.  I liked that Horlbeck16_ included a few thermodynamic features 
(sgRNA minimum free energy, predicted single-strandedness) that Doench16_ 
didn't (although Doench16_ did include melting temperatures for different parts 
of the spacer).  Ultimately, though, the top features were pretty similar 
between the two rules:

======================================= ==================================
Horlbeck16_                             Doench16_
======================================= ==================================
Target site position relative to TSS    Nucleotide dimers at each position
Nucleotide dimers at each position      Nucleotides at each position
Nucleotides at each position            Nucleotide dimer frequencies
Longest run of each base (e.g. TTTT)    Tm of positions 16-20
sgRNA folding minimum free energy       Amino acid cut position
======================================= ==================================

I chose to use the Doench16_ rules for two reasons.  First, I couldn't find a 
way to evaluate the Horlbeck16_ rules with only the features that are intrinsic 
to the sgRNA. In fact, it seemed prohibitively difficult to evaluate the 
Horlbeck16_ rules even with all the features, but maybe I could've gotten 
through that.  Second, the Doench16_ rules were trained on gene knock-out data, 
which is slightly more relevant to my project than the CRISPRi data that the 
Horlbeck16_ rules were trained on.

- Download the supplementary code from Doench16_::

      $ curl -O http://www.nature.com/nbt/journal/v34/n2/extref/nbt.3437-S3.zip

- Unpack the files::

      $ unzip nbt.3437-S3.zip
      $ tar -xzf Code/Rule_Set_2_Score.tar.gz

- Create a virtual environment to run the code in.  This is necessary both 
  because the script is ``python2`` and because it requires a very specific 
  version of ``scikit-learn`` in order to unpack its pickles::

      $ virtualenv -p python2.7 venv
      $ source venv/bin/activate

- Install the dependencies.  For some reason this has to be done in two steps::

      $ pip install numpy scipy pandas matplotlib biopython
      $ pip install scikit-learn==0.16.1

- The ``rs_score_calculator.py`` script has to be run from the directory it 
  lives in::

      $ cd Rule_Set_2_scoring_v1/analysis
      $ python rs2_score_calculator.py --seq AAAAAAAAAAAAAAAAAAAAAAAAAGGAAA
      Rule set 2 score: 0.2183

The Doench16_ rules take 30 bp sequences which contain some context before and 
after the spacer itself, specifically ``NNNN[spacer]NGGNNN``.  I need my 
spacers to start with ``GGG``, so I generated spacers from this pattern: 
``NNNNGGG[17×N]NGGNNN``.  I set the random seed to 0 to make the results 
reproducible.

I want to keep about half of the sequences I generate.  This is an arbitrary 
cutoff, but it feels stringent enough to remove most of the bad spacers and 
permissive enough to avoid introducing any significant bias.  I also want to 
pick spacers such that whether or not a spacer is included doesn't depend what 
other spacers were generated.  That way, if I decide I need to generate more 
spacers, I'll still have a simple script that produces all of the spacers I 
tested (which will be a nice way to prove that I didn't cherry-pick my 
spacers).  With this in mind, I scored 96 random spacers with the Doench16_ 
rules and found that the median was close to 0.5 (the scores can range from 0.0 
to 1.0).  So my algorithm for picking spacers became:

1. Set the random seed to 0.

2. Generate a uniformly random ``NNNNGGG[17×N]NGGNNN`` spacer.

3. Score the spacer using "rule set 2" from Doench16_.

4. If the spacer scores better than 0.5, keep it.  Otherwise don't.

5. Repeat steps 2-4 until I have the desired number of spacers.

This algorithm is implemented in the following script, which writes the 
resulting spacers to :download:`doench_spacers.tsv`::

    $ ssh guybrush
    $ cd ~kale/sgrna/notebook/20170329_test_multiple_spacers/doench16
    $ ./pick_doench16_spacers.py

Methods
=======

Primers d1--d8
--------------
Here are the primers for cloning the spacers into the 4kb pCR2.1 + AAVS 
plasmid.

.. command-output:: ./design_doench_primers.py 0:8
    :cwd: .

Here are the primers for replacing the J23119 promoter in my sgRNA plasmids 
with a T7 promoter:

.. command-output:: ../scripts/design_mutagenesis_primers.py
        J23119_TO_T7_GFP
        taaggatgatttctggaattctaaagatctTTGACAGCTAGCTCAGTCCTAGGTATAATACTAGTcatctaattcaacaagaattgtttcagagc
        taaggatgatttctggaattctaaagatctTATAGTAATAATACGACTCACTATAGcatctaattcaacaagaattgtttcagagc

Cloning d1--d4
--------------
`CR21` primers:

.. command-output:: ../protocols/general/pcr_cloning.py 8 60 -x 240

`J23119_TO_T7` primers:

Below is the protocol for 5 reactions (i.e. one spacer).  I setup different 
master mixes for each spacer.  Normally I would use a 2 min extension time for these plasmids, but I wanted to 
run the reactions in the same block as the ``CR21`` reactions:

.. command-output:: ../protocols/general/pcr_cloning.py 5 60 -x 240 -m primers

Linearize d1--d4
----------------
I had to do this twice because I used expired XmnI the first time and got 
incomplete cleavage.  It probably would've worked if I had just let it react 
longer, so in the future I should run a quick gel before stopping the reaction 
to make sure the digestion is complete.

.. include:: 20170508_linearize_cr21.txt
   :literal:

Transcribe d1--d4
-----------------
.. include:: 20170511_digest_pblo_for_t7.txt
   :literal:

.. include:: 20170511_transcribe_sgrna.txt
   :literal:

The in vitro transcription reactions worked very well.  The product was clean 
and the concentrations were high.  Most were around 1000 ng/μL, although the 
highest was 1921.1 ng/μL and the lowest was 627.4 ng/μL.

.. figure:: 20170511_transcribe_d1_d4.svg
   :width: 100%

Test d1--d4
-----------
.. include:: 20170512_cas9_cleavage_assay.txt
   :literal:

.. figure:: 20170512_test_d1_d4.svg
   :width: 100%

Looking at the data qualitatively, I would say that d1 and d4 worked well, d2 
worked weakly, and d3 didn't work.  What I'm not sure about is how to quantify 
this.  My initial instinct was to calculate a fold change: 

.. math::

   \frac{\mathrm{percent\ cleaved\ with\ theophylline}}{\mathrm{percent\ cleaved\ without\ theophylline}}

However, this metric basically just depends on how small the demonimator is, 
because the numerator can't be greater than 1.  So I don't really think fold 
change is appropriate here.

My second thought is just to subtract the percent cleavage in both conditions:

.. math::

   \mathrm{percent\ cleaved\ with\ theophylline} - \mathrm{percent\ cleaved\ without\ theophylline}

Cloning d9--d24
---------------
After cloning the first batch of spacers, I decided that 16 spacers was the 
most I could clone at once (thermocycler space is a big bottleneck).  With that 
in mind, here are the primers for the second batch of spacers.  I ordered them 
in a 96-well plate, because I think that'll make my life a little easier:

.. command-output:: ./design_doench_primers.py 8:24
    :cwd: .

I setup separate master mixes for each template, so each master mix was for 
only 8 reactions, but I had 48 reactions total.  I ran all the reactions with a 
4 min extension time, even though only the pCR21 reactions need it, just 
because I wanted to keep everything on one plate.

.. literalinclude:: 20170828_pcr_cloning.txt

Transcribe d9--d14 --- Sept 15, 2017
-------------------------------------
I wanted to transcribe RNA for d9--d16, but I realized after I started the 
reactions that I only had enough spin columns to purify 30 RNAs.  

d9/on has the wrong sequence (which you can see from the gel).  I forgot that 
we picked the wrong colony for this construct, and I never recloned it.  I'm on 
the fence about fixing this.  On the one hand, without the control I won't know 
if the reaction just doesn't work well.  On the other hand, there are controls 
for all the other spacers (so I'll know if nothing works) and I only really 
need data for the designs.

.. figure:: 20170915_transcribe_d9_d10.png

   Left: d9, Right: d10

.. figure:: 20170915_transcribe_d11_d12.png

   Left: d11, Right: d12

.. figure:: 20170915_transcribe_d13_d14.png

   Left: d13, Right: d14

Test d11--d14 --- Sept 16, 2017
-------------------------------
I'm not sure that I can use this data, because all the controls exhibit at 
least a little ligand-sensitivity.  I don't have any ideas about what could 
cause this effect, either.

.. figure:: 20170916_test_d11_d12.png

   Left: d11, Right: d12

.. figure:: 20170916_test_d13_d14.png

   Left: d13, Right: d14

Transcribe d17-d20 --- Sep 26, 2017
-----------------------------------
This was the first time I added RNase inhibitor to the reactions, and it seemed 
to improve the final product.  That implies that I do have RNase contamination.  
Assuming that the kit itself isn't contaminated (I think this is a reasonable 
assumption, since the problem has persisted over multiple kits), that means 
that either the DNA or the water is contaminated.

All of the reactions had low yields, although only d17 didn't have enough to 
make aliquots.  I'm wondering if the heated lid in the thermocycler is actually 
warming up the reaction past 37°C.

When I was measuring the RNA concentrations after the spin-column purification 
step, I noticed that most (all?) of the tubes had a precipitate at the bottom.  
I'm curious what it is.  If it's RNA, that could be good news or bad news.  On 
one hand, that would mean my yield would be higher.  On the other, why would my 
RNA precipitate?  It could also be the RNase inhibitor.  This is the first time 
I've ever seen a precipitate, and also the first time I've used this RNase 
inhibitor (the ampliscribe kit also has an RNase inhibitor, and I don't 
remember ever it ever producing a precipitate).  It could also be detritus from 
the spin columns: I used a new box of columns for these reactions; maybe 
they're from a bad batch.

.. figure:: ./20170926_transcribe_d18_d19.png

   Left: d18; Right: d19

.. figure:: ./20170926_transcribe_d20.png

   d20

Transcribe d21--d24 --- Sep 27, 2017
------------------------------------
I accidentally forgot to confirm the thermocycler for the overnight restriction 
digest, so instead of 1h at 37°C, 20m at 80°C, then holding at 12°C, the 
reaction was just at room temperature overnight.  I decided that that was 
probably fine and continued without repeating the incubation.

As with last time, the yields were low and the mysterious precipitate was 
present.  I didn't get enough RNA to aliquot either d22 or d23.  This is a 
recurring problem now, so I think I need to change some things to account for 
it.  First, I should elute the RNA in 25 μL of water.  I only really need 23.5 
μL of RNA: 5 μL for each of 4 aliquots (2 × 1.5 μL = 3 μL for the reactions, 2 
μL for pipetting error), 2 μL for the gel, and 1.5 μL for the nanodrop.  By 
eluting in 25 μL rather than 50 μL, I should have a better chance of getting 
the concentration I need.

Second, for repeat reactions, I should linearize 8 μL DNA rather than 4 μL.  
The reason I do 4 μL right now is so there's enough water in the reaction to 
make a master mix.  But that's not a concern when just repeating a few problem 
reactions.

Third, I should think about repeating the minipreps.  I can't remember for 
sure, but I think a lot of these preps were unusually low yield (e.g. 80 ng/μL 
rather than 300 ng/μL).  Maybe I didn't give the cells enough time to get 
saturated (I did effectively start all the cultures from ⅙ of a colony, and 
sometimes I started them growing pretty late).  If I get better minipreps, that 
could quadruple my RNA yield, which would put me back in a more comfortable 
range.

For this reaction, I used unopened RNase-free water from the new Zymo "RNA 
Clean & Concentrator-25" to eliminate the possibility that the water was the 
source of the RNase contamination.  The amount of degradation is about the same 
as with the old water though, so I don't think it is the culprit.

I'm going to attribute the high molecular-weight fragments (which I don't think 
I've ever seen before) to poor digestion of the DNA templates.

.. figure:: ./20170927_transcribe_d21_d24.png

   Left: d21; Right: d24

Transcribe d15--d17 --- Sep 29, 2017
------------------------------------
To account for the persistent trouble I've had getting RNA that's concentrated 
enough to aliquot, I made two changes to the protocol.  First, I added 4 μL of 
linearized DNA to the transcription reaction rather than 1 μL.  Second, I 
eluted the RNA from the Zymo spin columns in 25 μL nuclease-free water, rather 
than 50 μL.  These two changed helped, and I mostly got concentrations in the 
300--800 ng/μL range.  I also didn't observe any precipitate this time.

I let the transcription reaction go for 6h, because I was just busy with other 
things.

There's something wrong with d15/mhf/37.  I'm not sure what could cause a high 
molecular weight band like that.  In any case, I'm not planning to publish the 
mhf/37 data, so I'm not going to try to repeat or troubleshoot this.

There's more degradation than I expected.  I think this might be due to 
residual RNase A left over from the miniprep.  I'm already suspicious that the 
DNA is the source of the contamination, because the problem doesn't go away 
when I use new T7 kits or new nuclease-free water.  The most obvious way for 
the DNA to be contaminated is via the RNase A that's added in the first step of 
the miniprep.  I'm sure most of is is washed away, but perhaps some remains.

If this is the case, it makes sense that adding more template DNA would lead to 
more degradation.  But this also suggests a few ways to ameliorate the problem.  
First, if I decide to repeat the minipreps, I could do extra washes and/or try 
eluting in DEPC water.  Second, I could try boiling the DNA just before adding 
it the T7 reaction.  Boiling won't completely inactivate RNase A, because it 
can refold, but it may `inactivate some of it`__ (and I only expect to have 
trace amounts, as it is).  I already incubate the DNA at 80°C for 20 min to 
denature the restriction enzyme, but I usually do that in an overnight step 
that finishes ~10h before I start the T7 reaction, which may give the RNase 
time to refold.  Instead I'm envisioning 98°C for 5 min just before starting 
the reaction.
  
__ https://www.thermofisher.com/us/en/home/references/ambion-tech-support/nuclease-enzymes/tech-notes/rnase-and-depc-treatment.html

.. figure:: ./20170929_transcribe_d15_d16.png

   Left: d15; Right: d16

.. figure:: ./20170929_transcribe_d17.png

   d17

I also included d22/mhf/30 and d23/rxb/11/1 in the RNAs I transcribed today.  I 
didn't get enough of these RNAs to aliquot d22 or d23 two days ago.

.. figure:: ./20170929_transcribe_d22_d23.png

   Left: d22; Right: d23


Results
=======
Most --- but not all --- of the spacers are active.  In a real application, it 
will probably be necessary to test several spacers.

.. figure:: spacer_heatmap.svg
   :align: center

I was interested to see if base-pairing with the aptamer could explain why some 
spacers didn't work well.  To quantify this base-pairing, I calculated the 
minimum free energy (MFE) interaction between the spacer and the aptamer insert 
(i.e. the aptamer plus the screened random sequences on either side of it) 
using ViennaRNA.  

It's worth briefly noting that I used the `duplexfold()` function rather than 
the `mfe_dimer()` one.  The difference is that the former only considers 
inter-strand base-pairs, while the latter considers inter- and intra-strand 
pairs.  I decided that it was better to not consider intra-strand pairs.  
First, they could be misleading, because they would almost certainly be 
different in the context of the full sgRNA.  Second, my goal is to quantify a  
potential interaction between two strands, so I think it's better to focus only 
on inter-strand interactions.

The correlation between MFE predictions and experimentally-measured cleavage 
differences is fairly good for rxb/11/1.  In particular, the three really bad 
spacers (d5, d19, and d22) have the distinctly strongest MFE predictions.  I 
think it would be reasonable to say to that spacers with predicted affinity for 
the aptamer insert stronger than -18 kcal/mol should be avoided.

.. figure:: predict_spacer_quality.svg
   :align: center

To cross-validate this model, I calculated affinities for the in vitro screen 
spacer (aavs), the in vivo screen spacers (gfp, rfp, gfp2, rfp2) and the 
mammalian spacers (cf1, cf2, cf3).  All of these spacers work robustly in their 
respective assays except gfp2 and cf1, which do not work with any sensor.

======  =======================  =======================
Spacer  rxb affinity (kcal/mol)  mhf affinity (kcal/mol)
======  =======================  =======================
aavs                      -15.3                    -15.3
gfp                        -4.1                     -4.1
rfp                        -9.3                    -10.8
gfp2                       -6.1                     -3.3
rfp2                       -7.8                     -6.8
cf1                       -16.2                    -16.6
cf2                       -12.7                    -14.2
cf3                        -9.9                    -10.7
======  =======================  =======================

None of these spacers meet the -18 kcal/mol threshold for exclusion.  If we 
lower the threshold to -15 kcal/mol, then we would get:

- 1 true positive (cf1)
- 5 true negatives (gfp, rfp, rfp2, cf2, cf3)
- 1 false positive (aavs)
- 1 false negative (gfp2)

These results aren't very accurate and don't inspire much confidence in the 
model.  In particular, gfp2 is predicted to be the most active spacer.

Caveats
-------
- d9/on has the wrong sequence.  I would've been more worried about this if the 
  d9 designs had had poor cleavage, but they all had quite good cleavage.  The 
  makes the lack of a positive control less worrying (plus there were other 
  positive controls run at the same time, so I would've known if there had been 
  some problem with the reaction setup.

- The mixed up two of the control wells for the first replicate of d11.  The 
  wells go: d11 on (apo), d11 off (apo), d11 on (theo), d11 off (theo).

- I only have two good replicates for d19.  I also have two bad replicates, 
  where the controls exhibit a ~15% difference in response to theophylline.  
  I'm fairly confident that this is due to not mixing the sgRNA before adding 
  it to the reaction.  However, in all four cases there is no cleavage for any 
  of the designs.  The reason for this is pretty clear: the spacer base-pairs 
  significantly with the aptamer.  

  It wouldn't be trivial to repeat the reaction because I'm out of d19 sgRNA 
  and I'm also out of the T7 I'd need to make more.  Especially given that I'm 
  confident in the results for the designs, I don't think repeating this 
  experiment is worth it.


References
==========
.. [Doench14] Doench et al. *Rational design of highly active sgRNAs for 
   CRISPR-Cas9-mediated gene inactivation.*  Nat Biotechnol (2014) 
   32:12:1262-1267.
  
.. [Doench16] Doench et al. *Optimized sgRNA design to maximize activity and 
   minimize off-target effects of CRISPR-Cas9.* Nat Biotechnol (2016) 
   34:2:184-191.

.. [Horlbeck16] Horlbeck et al. *Compact and highly active next-generation 
   libraries for CRISPR-mediated gene repression and activation.*  eLife (2016) 
   5:e19760.

.. [RNase] RNase and DEPC Treatment: Fact or Laboratory Myth.  
   https://www.thermofisher.com/us/en/home/references/ambion-tech-support/nuclease-enzymes/tech-notes/rnase-and-depc-treatment.html
