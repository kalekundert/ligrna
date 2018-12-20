****************
Test w30 sensors
****************

The results from :expt:`20180122_test_m30_sensors` were not informative because I forgot 
to consider the active state when I was designing my mutants.  My goal in this 
experiment is to design and test a more informative set of mutations.

My plan is to make mutations to strand-swap base-pairs that we believe exist in 
the active state.  Assuming that these mutations have no effect on the active 
state itself, we can attribute the effects we observe to perturbations in the 
inactive state.  We will also test particular inactive state models by making 
additional mutations or swaps designed to rescue the deleterious effects of the 
each strand-swap.

We have two primary inactive state models that we're trying to distinguish 
between.  Model #1 was proposed by Kyle Watters based on his intuition and his 
(noisy) SHAPE-Seq data.  Model #2 is predicted by ViennaRNA:

.. figure:: proposed_models.svg

   http://rna.tbi.univie.ac.at/forna/

These models predict different effects for the various strand-swap mutations.  
Below is a table summarizing all of these predictions:

====  ==================================  ====================================
Swap  Model 1                             Model 2
====  ==================================  ====================================
63    No effect.                          Weaker off-state (maybe); rescued by
                                          swapping 78.
----  ----------------------------------  ------------------------------------
64    Weaker off-state; rescued by        No effect: lose 1 bp on the top,
      swapping 80                         gain 1 bp on the bottom.
----  ----------------------------------  ------------------------------------
65    Weaker off-state; rescued by C79G   Weaker off-state; cannot be rescued.
----  ----------------------------------  ------------------------------------
77    Weaker off-state; rescued by G67C.  Weaker off-state; rescued by G72C
----  ----------------------------------  ------------------------------------
78    Weaker off-state; rescued by U66G,  Weaker off-state; rescued by
      but that adds a lot of G's in a     swapping 63.
      row and may have other effects.
----  ----------------------------------  ------------------------------------
79    Weaker off-state; rescued by C79    No effect.
      (i.e. mutate A109C but not C79A)
----  ----------------------------------  ------------------------------------
80    Weaker off-state; rescued by        Stronger off-state.
      swapping 64.
====  ==================================  ====================================

There are a number of reasons why the data I collect for this experiment could 
be difficult or even impossible to analyze.  First, our model of the active 
state could be wrong.  It makes sense because it has stems matching the ones in 
wildtype sgRNA and it's the lowest energy conformation predicted by Vienna, but 
we don't have any experimental evidence for it.  Second, our assumption that 
strand-swap mutations won't affect the active state could be wrong.  In rxb/11, 
some functional strand-swap mutations were up to 3x less active than rxb/11 
itself.  Third, the mutations we're making could lead to the creation of 
alternative states that aren't populated in mhf/30.  For all these reasons, 
I'll have to do the data analysis very carefully.

I did consider the possibility of making mutations in the aptamer itself, but 
found that the entire core of the aptamer is conserved [Zimmermann2000]_.  
Mutating any position in the core would affect theophylline binding.  In some 
cases the effect would be as small as 2x, but I wasn't comfortable even with 
that because it's possible the effect would be larger in vivo that it is in 
vitro.

Results
=======
Executive summary:

- Most of the initial strand swaps were predicted to be more activating, but 
  instead all were either deactivating or about the same.

- The Model 1 rescue attempts most often had no significant effect.  The 
  exceptions are w30/64/2, which did significantly rescue function, and 
  w30/78/1, which significantly impaired function.

- The two Model 2 rescue attempts were both completely inactive.

- The base of the nexus stem (positions 63 and 71) was unexpectedly sensitive 
  to mutation.  The base of the nexus stem was also unexpectedly sensitive to 
  mutation in rxb/11/1, although this may or may not be related.

- There's no correlation between the activity of the mutants and the amount of 
  aptamer pre-folding predicted by ViennaRNA.

.. figure:: 20180222_test_w30.svg

   Flow cytometry traces for the w30 constructs.

w30/63 is interesting because I expected it to have a relatively weak effect on 
both models, but instead it had a very strong effect.  This is reminiscent of 
the effect at the base of the nexus stem for rxb/11/1, which I have still not 
been able to explain.  I simulated the w30/63 sequence in ViennaRNA to see if 
there were any obvious differences, but there weren't.

w30/64/1 was the best example of a rescue mutation that actually improved 
function.  I also compared this construct to w30/80, wince w30/64/1 is really 
just w30/64 and w30/80 at the same time.  w30/80 worked better than w30/64 and 
only a very little bit worse than w30/64/1.  So w30/64/1 did rescue both 
mutations, but not by very much.  

But I don't think I can conclude from this that Model 1 is correct, because 
neither w30/64 nor w30/80 behaved how that model predicted.  Both were expected 
to make the off-state weaker, and therefore to be more activating that mhf/30 
itself.  Instead, both were more deactivating.  This was actually a general 
problem: most of the initial strand swap mutants were predicted to be 
activating (for the simple reason that the swaps always preserved the number of 
base pairs in the active state model, but often base pairs in the inactive 
state models) but were in fact deactivating.  This was probably the most clear 
signal from the data, so if I were going to propose a mechanism, it'd have to 
explain why every mutation (even those that didn't have much of an effect of 
the dynamic range) was at least slightly deactivating.

w30/65 (along with w30/80) was notable for having a dynamic range pretty much 
the same as (if not bigger than) that of mhf/30.  65 and 80 are also the two 
positions that nearest to the top of their respective stems in the active-state 
model, but that may just be a coincidence.

It occurred to me while analyzing w30/65 that I should've also tested all the 
rescue mutations on their own.  A lot of the rescues are strand swaps, and I do 
have data for all those, but some (like this one) are single point mutants, and 
for those it's possible that the rescue mutation on it's own would've improved 
function.  In the end it didn't really matter, since w30/64/1 was the only 
example of a successful rescue, but it's something to keep in mind if I do 
something like this again.

w30/77 is one of the two positions that has a rescue mutation for both models.  
w30/77/1 did in fact slightly improve dynamic range, and w30/77/2 was totally 
inactive.  On its face this would seem to be an argument in favor of Model 1.  
However, Model 1 does not explain why the rescue mutation in w30/77/2 (G72C) 
would be deleterious, and again, both models incorrectly predict that w30/77 
would be more active than mhf/30.  For these reasons, I don't think any firm 
conclusions can be drawn from these mutants.

w30/78 is the other position that has a rescue mutation for both models.  
Although w30/78 itself has some activity (≈3x dynamic range), both rescue 
mutations are totally inactive.  The rescue mutation for w30/78/2 is swapping 
position 63, and we've already seen that that is deleterious for some unknown 
reason, but I can't justify the problem with the rescue mutation for w30/78/1 
(U66G).  (U68 is the one that we believe needs to interact with Cas9.)

w30/79 was reasonably active, and w30/79/1 didn't change that much.  The fact 
that w30/79 was reasonably active was more in line with the predictions for 
Model 2 than Model 1, but the predictions for the all the initial swaps have 
been so bad that I'm almost sure this is more a coincidence than anything else.

w30/80 had almost mhf/30 levels of activity.  It was also the only swap that 
was actually predicted (by Model 2 only) to be more inactive than mhf/30, but 
again I think the fact that it actually was is more of a coincidence than 
anything else.  m30/80/1 didn't rescue activity, but it didn't make it worse, 
either.

I didn't really find any support for Model 2.  I was only able to test two 
mutations (w30/63/2 and w30/78/2 are the same sequence), but both were totally 
inactive.  One of those was in the context of a totally inactivating 
strand-swap (w30/63), so maybe that shouldn't count as much, even though the 
point of the rescues was to *rescue*.  Either way, I feel fairly comfortable 
rejecting Model 2.

Model 1 is more inconclusive.  Most of the rescue mutations had no effect (i.e.  
didn't rescue but didn't impair).  While on one hand that wasn't what was 
predicted, on the other maybe it's an accomplishment just to maintain function 
in the face of 3-4 mutations.  In addition to all the "no effect" mutations, 
Model 1 also had one rescue that worked well, and one that imparied function.  
In my mind these are kind-of a wash.  I don't think there's enough evidence to 
reject Model 1, but I would hypothesize that it may be part of a more 
complicated conformational landscape.

One limitation of this analysis is that it only considers the two states that 
make up each model.  In reality, it's possible that every mutant is accessing a 
different set of states.  To test this, I tried running ViennaRNA predictions.  
The hypothesis for Model 2, to be a little more general, is that the aptamer 
needs to pre-form in order for ligand binding to occur.  So I calculated the 
free energy of the macrostate where the aptamer is formed and the free energy 
of the whole ensemble, and compared them to get a fraction of the ensemble in 
which the aptamer is preformed.  (All these simulations were done in the 
absence of the ligand, so the RNA wasn't getting a bonus for forming the 
aptamer.)  Here are the results:

.. literalinclude:: percent_prefolded.txt

It's hard to tell from this table, but these numbers don't correlate at all 
with the observed levels of activity.  It's not a very sophisticated model; it 
doesn't account for theophylline binding, folding kinetics, or the rest of the 
sgRNA being in the right conformation to bind Cas9.  But it does query the 
Model 1 hypothesis in a way that accounts for all other states, and comes up 
empty.

Methods
=======

Design primers
--------------
2018/02/08::

   $ ./design_primers.sh
   Number of oligos: 27

   Primer names (ready to copy into Elim form):
   GFP_W30_63_2_TM59_FOR, GFP_W30_78_2_TM59_FOR
   GFP_W30_63_2_TM59_REV, GFP_W30_78_2_TM59_REV
   GFP_W30_63_TM59_REV
   GFP_W30_63_TM60_FOR
   GFP_W30_64_1_TM59_REV, GFP_W30_80_1_TM59_REV
   GFP_W30_64_1_TM62_FOR, GFP_W30_80_1_TM62_FOR
   GFP_W30_64_TM59_REV
   GFP_W30_64_TM60_FOR
   GFP_W30_65_1_TM60_FOR
   GFP_W30_65_1_TM60_REV
   GFP_W30_65_TM60_REV
   GFP_W30_65_TM61_FOR
   GFP_W30_77_1_TM58_FOR
   GFP_W30_77_1_TM60_REV
   GFP_W30_77_2_TM58_FOR
   GFP_W30_77_2_TM60_REV
   GFP_W30_77_TM58_FOR
   GFP_W30_77_TM59_REV
   GFP_W30_78_1_TM59_FOR
   GFP_W30_78_1_TM59_REV
   GFP_W30_78_TM59_FOR
   GFP_W30_78_TM60_REV
   GFP_W30_79_1_TM60_REV
   GFP_W30_79_1_TM61_FOR, GFP_W30_79_TM61_FOR
   GFP_W30_79_TM60_REV
   GFP_W30_80_TM59_REV
   GFP_W30_80_TM62_FOR

   Primer sequences (ready to copy into Elim form):
   ATACCAGCCGAAAGGCCCTTGGCAGCGAGggcaccgagtcgg
   CGGGGTATACCGGACACCGttatttcaacttgctatgctgt
   CGttatttcaacttgctatgctgt
   GTGTCCGgtatacgccgataccagc
   CCGCGTATACGCGACACGcttatttcaacttgctatgctg
   ATACCAGCCGAAAGGCCCTTGGCAGCCacggcaccgagtcg
   Gcttatttcaacttgctatgctg
   GTGTCGcgtatacgccgatacca
   CCGTATACGGcgataccagccgaaag
   CACAGccttatttcaacttgctatgc
   ccttatttcaacttgctatgc
   CTGTGccgtatacgccgatacc
   CCAGCCGAAAGGCCCTTGGCAGCGACCgcaccgagtcggtg
   TATCGGCCTATACGGGAGacccttatttcaacttgctatg
   CCGAAAGGCCCTTGGCAGCGACCgcaccgagtcggtg
   CTGGTATCGGCCTATAGgggacacccttatttcaac
   GAAAGGCCCTTGGCAGCGACCgcaccgagtcggtg
   GGCTGGTATCGGCCtatacgggacacccttattt
   ACCAGCCGAAAGGCCCTTGGCAGCGAGggcaccgagtcgg
   ATCGGGGTATACGGGACCcccttatttcaacttgctatg
   CGAAAGGCCCTTGGCAGCGAGggcaccgagtcgg
   GCTGGTATCGGGgtatacgggacacccttattt
   CGGCTGGTATCGGcgtatacgggacaccct
   AAAGGCCCTTGGCAGCGCcggcaccgagtcg
   CGGCTGGTATCGTcgtatacgggacaccct
   TCGGCTGGTATCCgcgtatacgggacacc
   AAGGCCCTTGGCAGCCacggcaccgagtcg

Cloning
-------
2018/02/13:

I needed to optimize melting temperature for w30/63 and w30/64:

w30/63
   I got some product at 68°C (the highest temperature in the gradient), but 
   not a lot, and there did appear to be minor products.  I didn't get any 
   product at lower temperatures.

w30/64
   I got the most product at 53°C (the lowest temperature in the gradient), but 
   even then not a lot.  I got some product at temperatures as high as 60°C.
    
For both of these difficult reactions, I transformed 100 μL of competent cells 
with 10 μL of ligation reaction (because the PCR bands looked so weak), and got 
a reasonable number of colonies.

.. literalinclude:: 20180213_pcr_cloning.txt

Flow cytometry
--------------
Biological replicates on 2018/02/22, 2018/02/23, and 2018/02/24.  For the three 
replicates, I grew the cells for 8h15, 8h05, and 8h10 respectively.  All 
experiments were done in 24-well blocks.

.. literalinclude:: 20180301_crispri_assay.txt

   
References
==========
.. [Zimmermann2000] :doi:`10.1017/S1355838200000169`
