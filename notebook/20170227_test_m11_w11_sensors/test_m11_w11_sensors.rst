************************
Test m11 and w11 sensors
************************

The ``w11`` and ``m11`` design strategies is based off the hypothesis that 
``rxb 11,1`` works by controlling the ability of U94 (which corresponds to U59 
in wt sgRNA) to flip out and interact with Cas9.  In turn, this hypothesis is 
based on the claim made by Kyle Watters (citing unpublished data) that wildtype 
sgRNA can only bind Cas9 if U59 is unpaired.

In ``rxb 11,1``, U94 forms a wobble base pair in the middle of a 5 bp stem.  
The hypothesis is that when no ligand is present, the base of the aptamer comes 
apart and allows the top of the stem to melt, which allows U94 to flip out and 
interact with Cas9.  When ligand is present, the base of the aptamer comes 
together, locks the stem in place, and prevents U94 from flipping out.

.. figure:: rxb_11_1_mechanism.svg
    :align: center
    :width: 300 px

If this hypothesis is correct, swapping G64 and U94 should have a severe 
detrimental effect on the sensor, because U94 will no longer be in a position 
to interact with Cas9 (despite the fact that this mutation does not change the 
strength of the nexus stem).  But swapping any of the other base pairs in the 
nexus stem should have no effect.  This is what the ``w11`` designs will test.

If this hypothesis is correct, we should also be able to modulate how well 
``rxb 11,1`` turns on or off by increasing or decreasing, respectively, the 
strength of the base pairs above it.  For example, replacing one or both of the 
GC base pairs with AU base pairs should allow the top of the stem to melt more 
easily, which should create a sensor that turns on better.  Likewise, 
increasing the length of the stem should make it harder for U59 to flip out, 
which should create a sensor that turns off better.  This is what the ``m11`` 
designs will test.

Designs ``m11`` primers
=======================
.. command-output::
    ../scripts/clone_into_sgrna.py
        m11/ga
        m11/gu
        m11/gh
        m11/gv
        m11/gga
        m11/ggu
        m11/ggh
        m11/ggv

Design ``w11`` primers
======================
.. command-output::
    ../scripts/clone_into_sgrna.py
        w11/1
        w11/2
        w11/4
        w11/5

Protocol
========
.. command-output::
    ../protocols/crispri_assay.py -t 8h30

I repeated this assay on three different days (3/15, 3/17, 3/21), each time 
using freshly picked colonies.  I made a particular effort to grow the cells 
for the exact same amount of time each time, because I thought getting the time 
exactly right would help lower the error bars.

Analysis
========

.. figure:: 20170315_test_w11_m11.svg

    GFP fluorescence normalized by RFP fluorescence.  Fold changes calculated 
    from the modes of the apo and holo distributions.

It's surprising that ``w11 1`` is always off.  Briner14_ didn't swap that 
particular base pair, but they did replace it with AU and saw almost no effect.  
(They also replaced the base pair above it with AU and again saw no effect.)  
So it seems unlikely that that base pair is especially important to the 
wildtype sgRNA.  The remaining possibilities (that I can think of) are that 
that base pair is playing a role in the ``rxb 11,1`` mechanism that I don't 
understand, or that I made a mistake cloning the ``w11 1`` construct.  Just to 
be safe, I should re-sequence that plasmid.

.. update:: Apr 5, 2017

    I sent the plasmid for resequencing and it came back correct.  It's still 
    possible that I accidentally transformed the wrong plasmid (e.g. ``off`` 
    instead of ``w11 1``), but unfortunately I already threw out my plates, so 
    the only way to check would be to re-transform the plasmid and to redo the 
    CRISPRi assay.  Frankly, that's too much work to check for a mistake I 
    probably didn't make.

.. update:: Apr 24, 2017

    Tanja convinced me that it was important to be absolutely certain that this 
    result wasn't a mistake, so I re-transformed the plasmid and redid the 
    CRISPRi assay.  I also sequenced the same cells I used for the assay.  All 
    the results were the same, and all the sequencing came back correct.  This 
    is chronicled in :doc:`/20170420_understand_w11_1/understand_w11_1`.

Other than ``w11 1``, the rest of the ``w11`` designs agree with my proposed 
mechanism.  ``w11 3`` is inactive (because U94 is on the wrong side of the 
stem) and the rest are active.  It is noteworthy that none of the 
strand-swapped designs are as active as ``rxb 11,1`` because this is not 
explained by my hypothesis.  One possible explanation (provided by Fitzy) is 
that ``rxb 11,1`` has mostly pyrimidines on the 3' side.  Pyrimidines are less 
bulky than purines, so this may afford U94 a bit more space to flip out.  That 
said, I'm not sure how to test this explanation, or what some other 
explanations could be.

The ``m11`` designs also support my hypothesis.  In the plot above, the designs 
are arranged from weakest to strongest stems (from top to bottom).  As 
expected, the designs with the weaker stems look more like the positive control 
and those with the stronger stem look more like the negative control.  The 
diagonal pattern is pretty clear.  Furthermore, ``m11 ga`` may be useful in 
it's own right.  Even though it's fold change is slightly smaller than ``rxb 
11,1``, it turns on better.  ``w11 2`` may also be useful in cases where the 
sgRNA needs to turn all the way off.

Testing ``w11 2,g``
===================
After I showed this data to Christof, he suggested that I try replacing the UA 
base pair (second from the bottom of the stem) with GC, which is the wildtype 
base pair at that position.  He thought it might work better since it's "more 
wildtype", or it might shine some more light on my proposed mechanism.  It 
seems like a reasonable thing to try.  I figure I'll try the CG base pair while 
I'm at it.  Below are the primers I ordered:

.. command-output::
    ../scripts/clone_into_sgrna.py
        w11/2/g
        w11/2/c

I followed the exact same protocol as before.  Here are the data I collected:

.. figure:: 20170418_test_w11_2_gc.svg

Supplemental figure
===================
I spent some time tweaking this figure in ``inkscape`` to get it ready for the 
supplement.  The final version of the figure (with a caption) is below:

.. figure:: paper/20170315_test_w11_m11_figure.svg
    
    Mutational analysis of ``rxb 11,1``.
    [left panels] Cell populations in the presence (solid lines) and absence 
    (dashed lines) of theophylline.  We used flow cytometry to measure 
    fluorescence values for individual cells, and we used Gaussian kernel 
    density estimation (KDE) to calculate population distributions.  The x-axis 
    shows GFP fluorescence divided by RFP fluorescence.  The sgRNAs target GFP, 
    and RFP is being expressed as an internal control for cell size.  The modes 
    of the populations are indicated by the plus-signs below the plots.
    [right panels] Ligand-induced fold changes in fluorescence.  Specifically, 
    fold change is the ratio of the modes of the apo and holo populations for 
    the sensor in question.  [a] Proposed mechanism.  [b] Crystal structure of 
    Cas9 showing the uracil in the nexus flipped out and buried in Cas9.  [c] 
    The positive control, the negative control (an sgRNA with the 5' side of 
    the nexus stem mutated to CC), and ``rxb 11,1``.  [d] Variants of ``rxb 
    11,1`` where the highlighted base pairs have been strand swapped.  [e] 
    Variants of ``rxb 11,1`` that attempt to modulate sensor activity by either 
    weakening or strengthening the stem above the uracil that is believed to 
    flip out to interact with Cas9.  The variants are sorted from weakest to 
    strongest.  [labels] The uracil believed to be important for Cas9 binding 
    is marked with an arrow.  Mutations relative to rxb/11/1 are highlighted in 
    yellow.  

.. [Briner14] Briner et al. Guide RNA functional modules direct Cas9 activity 
   and orthogonality.  Mol Cell (2014) 56:333-339.
