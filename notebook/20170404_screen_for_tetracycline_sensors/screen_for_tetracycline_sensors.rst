*******************************
Screen for tetracycline sensors
*******************************

Picking an aptamer
==================
I used the aptamer described in Wittman11_.  Win07_ and Weigand07_ also used 
``tet`` aptamers for synthetic biology, but with slightly different sequences.  
The sequence from Win07_ differed from Wittman11_ by A59U.  Maybe both 
sequences work, but I have more confidence that Wittman11_ isn't a typo because 
I got that sequence from primers given in the results section, while I had to 
transcribe Win07_ from looking at figure 6.  The sequence from Weigand07_ used 
GAAA to cap P2 instead UUCG.  But both of these papers are from the Suess lab, 
so I trust the most recent paper to be the best aptamer they're aware of.

The only thing I'm waffling about is whether to include any of stem P1 in my 
aptamer.  Weigand07_ suggests that P1 needs to be 6-7 bp long to get effective 
regulation, and that's too long for my libraries to reach without help.  
Wittman11_ just randomizes 5 bps without keeping any of P1 (although they do 
give it one base pair at the bottom of the stem).  I wouldn't worry about this 
with bacteria, but with yeast my libraries are ≈100x smaller.  Still, there are 
a lot of ways to make base-paired RNA, so I think I'll be fine not keeping any 
of P1.

Win07_ is bullshit
==================
It bears emphasizing that Win07_ is bullshit because it redefines the term 
"fold" in a misleading way.  Chen09_ discusses this paper and why its use of 
the term fold is misleading:

    More recently, the engineering of artificial riboswitches based on 
    cis-cleaving aptazymes has achieved some success. By connecting the 
    anti-theophylline or anti-tetracycline aptamers to the tobacco ringspot 
    virus (TRSV) HHRz via rationally designed or selected communication 
    modules, Win and Smolke engineered aptazymes that, when inserted to the 39 
    UTR of the GFP gene, could regulate GFP expression in yeast in response to 
    theophylline or tetracycline concentration [14]. The reported dynamic range 
    of GFP expression level was 20,25-fold (Figure 2 of [14]). However, closer 
    inspection of the raw data provided in the supplementary material (Figure 
    S13 of [14]) showed that the dynamic range of GFP expression level was 
    actually much lower. Among all the aptazyme constructs that were designed 
    and tested, most displayed only ~1.5-fold regulation and the best ones 
    displayed ~2.5-fold regulation. The discrepancy between the interpretation 
    and the data was due to redefinition of the word ‘fold’ by the authors.  
    Although the word ‘fold’ is generally used to express the ratio of two 
    quantities, Win and Smolke used ‘fold’ as a unit of absolute quantity of 
    GFP expression [14]. For example, the GFP expression level from an 
    unengineered plasmid was defined as ‘50 fold.’ Therefore, when the GFP 
    expression level from an engineered plasmid changed from ‘20 fold’ in the 
    absence of theophylline to ‘43 fold’ in the presence of theophylline, a 
    dynamic range of ‘(43 - 20 = ) 23 fold’ could be claimed. Most researchers 
    would instead estimate the dynamic range to be (43 / 20 = ) 2.2-fold. Win 
    and Smolke have also reported that multiple aptazymes inserted into the 39 
    UTR could act as logic gates for gene expression, but the raw data 
    necessary to evaluate these claims were not immediately available [15].

Rationally sequestering the nexus uracil
========================================
Figure 5 in Weigand07_ suggests that the ``tet`` aptamer might work really well 
with ``rxb 11,1``:

.. figure:: weigand07_fig_5.png

Here the nucleotides in the blue box are the splice site that Weigand07_ are 
trying to regulate.  But notice that U75 on the 3' side of P1 appears to be 
sequestered by ligand binding.  That's the exact same mechanism by which ``rxb 
11,1`` works, so many it's worth trying a few rational designs with exactly 
this sequence.

Ordering Primers
================
I'm going to use the same forward and backward libraries for the tetracycline 
aptamer as I did for the neomycin aptamer:

.. literalinclude:: primers.txt

Library transformations
=======================
.. electrotransformation::

   tdh1 tet ux 3,2:
      colonies: x 72 5 0
   tdh1 tet ux 4,3:
      colonies: x 81 16 1
   tdh1 tet ux 5,4:
      colonies: x 94 11 3

   tdh1 tet rhi 4,4:
      conc: 99.6 ng/μL
      colonies: x 46 2 0
   tdh1 tet rhi 4,5:
      conc: 114.4 ng/μL
      colonies: x 75 11 0
   tdh1 tet rhi 5,4:
      conc: 60.7 ng/μL
      colonies: x 19 2 0
   tdh1 tet rhi 5,5:
      conc: 68.8 ng/μL
      colonies: x 40 5 0
      recover: 2200 μL

Sequencing looks perfect for both libraries.

References
==========
.. [Weigand07] Weigand and Suess.  Tetracycline aptamer-controlled regulation 
   of pre-mRNA splicing in yeast. Nucleic Acids Research (2007) 35:12:4179.

.. [Win07] Win and Smolke. A modular and extensible RNA-based gene-regulatory 
   platform for engineering cellular function. PNAS (2007) 104:36:14283-88.

.. [Chen09] Chen and Ellington. Design principles for ligand-sensing, 
   conformation-switching ribozymes.  PLoS Comp Biol (2009) 5:12.

.. [Wittman11] Wittman and Suess.  Selection of tetracycline inducible 
   self-cleaving ribozymes as synthetic devices for gene regulation in yeast.  
   Mol BioSyst (2011) 7:2419-2427.

