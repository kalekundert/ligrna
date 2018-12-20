****************
Test m30 sensors
****************

After analyzing the SHAPE-seq data, Kyle W. proposed a model for how mhf/30 
works.  In this model, the inactive state contains a partially folded aptamer 
and a misfolded nexus that ends in a base pair between G64 and C80.  The active 
state contains the fully folded base pair, on top of a stem that includes a 
base pair between C80 and G108.  If this model is correct, it's essential that 
both G64 and G108 can both form strong base pairs with C80.  We can test this 
by mutating each of these positions one by one.  In particular, below are the 
mutants we want to test:

==  ==  ===  ===============================================================
64  80  108  Predicted effect
==  ==  ===  ===============================================================
G   C   G    This is the wildtype sequence.
G   C   C    This should be "always off", because the base pair
             characterizing the active state has been eliminated.
G   G   C    This should be "always on", because the base-pair 
             characterizing the active state has been rescued at the
             expense of the base-pair characterizing the inactive state.
C   G   C    This should respond to ligand like mhf/30, because the
             base-pairs characterizing both the active and inactive states
             have been rescued.
==  ==  ===  ===============================================================

.. update:: 2018/02/08

   After doing this experiment, I realized that the mutants were not smartly  
   chosen.  See the `Results`_ section for details.

Results
=======
1. There is a base pair between C80 and G108 that is critical for Cas9 
   activity.  This explains why mutating G108 (gcc) breaks the sensor and why 
   making a compensatory mutation to C80 (ggc) rescues it.  However, this is 
   not surprising.  

2. The G64C mutation (cgc) is not informative, because it breaks a base pair in 
   the middle of the nexus.  When I designed this mutation, I was thinking only 
   of the inactive (apo) state and forgot to consider the effect in would have 
   on the active (holo) state, which in this case was significant.

   This mutation would've been informative if I'd also made the C70G mutation, 
   which would maintain the G64--C70 base pair present in the active state.  I 
   included this mutation in my next round of constructs: w30/80/1

.. figure:: 20180206_test_m30.svg

For what it's worth, ViennaRNA correctly predicts which of these constructs are 
active.  The fact that m30/ggc is shifted towards the off state is more 
consistent with the Vienna model (#2) than the Watters model (#1).  The Vienna 
model predicts that the swap would strengthen to inactive state by allowing it 
to form a base pair that it previously couldn't.  The Watters model predicts 
that the swap would weaken the off state by disrupting a base-pair that would 
otherwise exist.

Methods
=======

Primers
-------
2018/01/22:

.. literalinclude:: 20180122_clone_into_sgrna.txt

2018/01/25:

.. literalinclude:: 20180125_pcr_cloning.txt

2018/02/06:

I grew the cells in a 24-well block, since large wells are important to get 
reproducible data.  I grew the overnight and the day cultures in the same 
block, because there was space.

.. literalinclude:: 20180206_crispri_assay.txt

