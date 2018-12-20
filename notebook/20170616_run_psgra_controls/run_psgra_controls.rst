******************
Run pSGRA controls
******************

After my last group meeting, Tanja and others thought that I should give the 
*in vivo* spacer assay (using the pSGRA plasmid shown below) another try.

.. figure:: sbol_diagram.svg
   :width: 80%
   :align: center

The reason is that the results from the *in vitro* spacer assay are not very 
striking, and there are questions about how well the *in vitro* and *in vivo* 
data correspond anyway.  The previous controls I ran with the pSGRA construct 
(which I called pN20 at the time) were not very conclusive, either, so it's 
still very possible that this experiment could work.

The first thing I want to try is a positive control sgRNA that targets GFP 
itself, and that doesn't include a PAM.  This really tests the best possible 
repression I could get with this system, and controls for targeting so far 
before the GFP gene and inserting a PAM into the sgRNA.

I also want to try a more exhaustive time course.  This is important because 
the osmY promoter is induced when the cells hit stationary phase, which they're 
just getting to after 9h.

Protocol
========
I designed primers to clone the `gfp on` control using the `n20 on` control as 
a backbone:

.. literalinclude:: 20170616_design_mutagenesis_primers.txt

.. literalinclude:: 20170627_crispri_assay.txt

Results
=======
With the `gfp on` sgRNA, the system gets nearly as good repression as I observe 
with the genomically encoded fluorescent proteins.  I want to repeat this 
experiment with `aavs on`, so I can also compare its repression to that of `gfp 
on`.

.. figure:: 20170626_psgra_controls.svg
   :width: 80%
   :align: center

   The dashed lines are the `off` constructs, and solid lines are the `on` 
   constructs.  The y-axis indicates how much overnight culture was diluted 
   into 1 mL media for the experiment.

The other thing to note is that the results don't seem to change the longer the 
cells have been in stationary phase.  I only measured one time point, but I  
made different initial dilutions to get cultures that spent different amount of 
time in stationary phase.  All four dilutions looked equivalent on the flow 
cytometer, even though the more concentrated dilutions were clearly more 
strongly colored by visual inspection.

Another oddity was that the `on` cultures were clearly more green than the 
`off` cultures by eye.  This is the opposite of what I would've expected, and 
I'm not sure what to make of it.

Degradation tag
===============
I began wondering if this system would benefit significantly from adding a 
degradation tag to the fluorescent proteins.  My concern is that I'm using a 
promoter that's induced when the cells reach stationary phase.  The advantage 
of this system is that cells with better repression won't have a growth 
advantage over those that don't.  (Such a growth advantage would confound the 
results I hope to get from this assay.)  The drawback is that once cells start 
producing fluorescent protein, they're no longer dividing to dilute it.  
Assuming that the fluorescent proteins have long half-lives in the cytoplasm, I 
may not be able to reach the state where protein production balances protein 
degradation.  This could make it hard to compare experiments, or make the 
timing of the experiments very critical.  Adding a degradation tag to the 
proteins could give me the best of both worlds: a system where repression 
doesn't affect cell growth, and where protein production and degradation can 
reach a rapid equilibrium.

The protein degradation system used for synthetic biology in E. coli is based 
on the peptide attached to stalled proteins by the ssRA (aka tmRNA) ribosome 
rescue system [Janssen12]_.  tmRNA is an RNA that binds to stalled ribosomes, 
frees the ribosome from the mRNA it choked on, then provides a new ORF with 
which to complete the nascent protein.  This ORF encodes an 11-residue 
degradation tag followed by a stop codon.  The consensus sequence for this tag 
is `AANDENYALAA`.  [Anderson98]_ experimented with four variants of this tag, 
and found that they give rise to different protein half-lives.  I found a fifth 
variant on the `IGEM parts list`__, which was just listed as being "moderately 
fast" (the consensus sequence was listed as "very fast"):

===============  =================
Variant                  Half-life
===============  =================
`AANDENYALAA`               40 min
`AANDENYALVA`               40 min
`AANDENYAAAV`               60 min
`AANDENYAASV`              110 min
`AANDENYADAS`    "moderately fast"
===============  =================

__ http://parts.igem.org/Protein_domains/Degradation

To put these half-lives in perspective, sfGFP folds and becomes fluorescent 
within 4 min [Pedelacq05]_ and degrades on its own at a negligible rate 
[Tombolini97]_.  I'm not sure how fast the osmY promoter expresses protein or 
how much fluorescent protein is required for a strong signal, though.

I used `IDT's codon optimization tool`__ to get a DNA sequence for each ssRA 
tag that I want to try.  I left out `LVA` because it has the same half-life as 
the consensus sequence.  I used the "Map Codons Only" button rather than the 
"Optimize" button, so these sequences are just the most likely codon for each 
amino acid.  I didn't want to use "Optimize" because it isn't deterministic, so 
I wouldn't be able to reuse the reverse primers:

=============  =============================================
Variant        Codon-optimized DNA sequence
=============  =============================================
`AANDENYALAA`  `GCG GCG AAC GAT GAA AAC TAT GCG CTG GCG GCG`
`AANDENYAAAV`  `GCG GCG AAC GAT GAA AAC TAT GCG GCG GCG GTG`
`AANDENYAASV`  `GCG GCG AAC GAT GAA AAC TAT GCG GCG AGC GTG`
`AANDENYADAS`  `GCG GCG AAC GAT GAA AAC TAT GCG GAT GCG AGC`
=============  =============================================

__ https://www.idtdna.com/CodonOpt

I designed inverse PCR primers to clone these tags into pSGRA after both GFP 
and RFP:

.. literalinclude:: 20170623_gfp_ssra_primers.txt

.. literalinclude:: 20170623_rfp_ssra_primers.txt

Unfortunately, there's a problem here.  The forward primers are the same for 
both fluorophores, because they both have the same terminator, so I can't use 
inverse PCR to install the degradation tags.  At the moment, I can't think of 
another easy way to cone these constructs.  Maybe 


References
==========
.. [Janssen12] Brian Janssen and Christopher Hayes. The tmRNA ribosome-rescue 
   system. Adv Protein Chem Struct Biol (2012) 86:151–191.

.. [Anderson98] Jens Anderson et al. New Unstable Variants of Green Fluorescent 
   Protein for Studies of Transient Gene Expression in Bacteria. Appl Environ 
   Microbiol (1998) 64(6):2240–2246.

.. [Tombolini97] Tombolini, Unge, Davey, de Bruijn, Jansson.  Flow cytometric 
   and microscopic analysis of GFP-tagged Pseudomonas fluorescens bacteria.  
   FEMS Microbiol Ecol (1997) 22:17–28. 

.. [Pedelacq05] Pédelacq, Cabantous, Tran, Terwilliger, Waldo.  Engineering and 
   characterization of a superfolder green fluorescent protein. Nat Biotechnol 
   (2005) 24:79–88.

