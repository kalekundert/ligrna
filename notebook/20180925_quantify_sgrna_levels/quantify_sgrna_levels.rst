*********************
Quantify sgRNA levels
*********************

Methods
=======
2018/09/25:

Fitzy found primers for the loading controls and sfGFP (not necessary for this 
experiment, but we ordered it at the same time):

16S rRNA:

- QPCR_16S_FWD: CTCTTGCCATCGGATGTGCCCA
- QPCR_16S_REV: CCAGTGTGGCTGGTCATCCTCTCA

ihfB:

- Fwd: GCGGTTTCGGCAGTTTCT
- Rev: CGCAGTTCTTTACCAGGTTT

sfGFP:

- QPCR_GFP_FWD: GTTCCGTGGCCAACACTTGTCACT
- QPCR_GFP_REV: TACATAACCTTCGGGCATGGCACT

I designed primers for the sgRNAs by hand:

:download:`qpcr_primers.xlsx`

Extract RNA
-----------
2018/09/28:

1. Start overnight cultures in 2 mL LB + Carb + Chlor for each of the following 
   constructs:

   - j23119 : g1 on
   - j23119 : g1 off
   - j23119 : g1 mhf 30
   - j23119 : g1 rxb 11,1
   - j23150 : g1 on
   - j23150 : g1 off
   - j23150 : g1 mhf 30
   - j23150 : g1 rxb 11,1

2. Incubate at 37°C overnight.

2018/09/29:

1. For each construct, inoculate 5 mL EZCCA and 5 mL EZCCAT with 100µL 
   overnight culture.

2. Incubate at 37°C for 2h.

3. Extract total cellular RNA:

   - Pellet cells at 4100 rpm for 10 min.
   - Resuspend each cell pellet in 1 mL TRIzol (Invitrogen 15596026).
   - Incubate 5 min at room temperature.
   - Add 200 µL chloroform.
   - Vortex vigorously.
   - Centrifuge for 15 min at 20,000g and 4°C.
   - Transfer aqueous phase (top, not pink, ~500 µL) for each sample to a clean 
     tube, taking care to avoid transferring any of the organic phase.

4. Concentrate and purify the RNA by ethanol precipitation:

   - Add 1 µL GlycoBlue (Invitrogen AM9516) to each sample.
   - Add 500 µL isopropanol.
   - Incubate at room temperature for 10 min.
   - Pellet for 20 min at 12,000g and 4°C.
   - Carefully pipet off all supernatant.
   - Resuspend pellet in 70% EtOH.
   - Vortex briefly
   - Pellet for 5 min at 7,500g and 4°C.
   - Carefully pipet off all supernatant.
   - Air dry for 10 min.
   - Resuspend RNA in 10 µL water.

5. Measure the RNA concentration of each sample using the Nanodrop.  Yield:

   ========  ===========  ======  =====
   Promoter  sgRNA        Ligand  ng/µL
   ========  ===========  ======  =====
   j23119    g1 on        apo       489
   j23119    g1 on        holo      616
   j23119    g1 off       apo       337
   j23119    g1 off       holo      515
   j23150    g1 rxb 11,1  apo       469
   j23150    g1 rxb 11,1  holo      603
   j23150    g1 mhf 30    apo       497
   j23119    g1 mhf 30    holo      636
   j23119    g1 on        apo       692
   j23119    g1 on        holo      671
   j23119    g1 off       apo       395
   j23150    g1 off       holo      477
   j23150    g1 rxb 11,1  apo       486
   j23150    g1 rxb 11,1  holo      434
   j23150    g1 mhf 30    apo       397
   j23150    g1 mhf 30    holo      426
   ========  ===========  ======  =====

Reverse transcription
---------------------
2018/09/29:

1. Setup reverse transcription reactions for each sample:

   - 1 µg RNA
   - 2 µL SuperScript VILO master mix (Invitrogen 11755050)
   - water to 10 µL

   The master mix contains random hexamers, which will prime the reverse 
   transcription of all RNAs in the sample.

2. Incubate at the following temperatures:

   - 25°C for 10 min
   - 50°C for 10 min (15 min)
   - 85°C for 5 min
   - hold at 4°C

Validate primers
----------------
2018/10/01:

The qPCR reagent is expensive, so we first want to make sure our primers work 
well and are specific for our sgRNAs in regular PCR.

1. Design and order a handful of possible forward and reverse primers.

   In this experiment, I had 3 forward primers, 2 reverse primers for all the 
   sgRNAs excpet mhf/30, and 3 reverse primers for mhf/30.  This made for a 
   total of 15 pairs of primers.

3. Dilute reverse transcription reactions to 100 µL (i.e. add 90 µL 
   nuclease-free water).

2. Setup PCR reactions for each pair of primers::

      Reagent        Conc     Each    8x MM    8x MM
      ──────────────────────────────────────────────
      water                 3.8 μL  30.4 μL  38.0 μL
      cDNA*                 0.2 μL
      primer mix    10 µM   1.0 μL
      polymerase**     2x   5.0 μL  40.0 μL  50.0 μL
      ──────────────────────────────────────────────
                           10.0 μL        9.0 μL/rxn

   \*Unknown concentration because sample was not purified and contains RNA, 
   DNA, and nucleotides.  \**NEBNext High-Fidelity 2x PCR master mix (NEB 
   M0541S)

3. Run the following thermocycler protocol:

   - 98°C for 30 sec
   - 35 cycles:
      - 98°C for 10 sec
      - 60°C for 20 sec
      - 72°C for 15 sec
   - 72°C for 2 min

4. Run the reactions on a 2% agarose gel to visualize 
   product.

.. figure:: 20181001_validate_sgrna_qpcr_primers.svg
   :width: 400px

   PCR products for all primer pairs.  Top: g1/rxb/11/1 template.  Bottom: 
   g1/mhf/30 template.  The primer names (9, 15, 26, 77, 90, 52+, 66+, 74+) 
   refer to the offset of the primer from the start of the sgRNA (including the 
   spacer).  The "+" nomenclature indicates the reverse primers that are 
   specific for mhf/30.  The primer pairs chosen for use in qPCR are marked by 
   "*".  Note that the gel is quite sensitive to small changes in amplicon 
   size.

qPCR
----
2018/10/02:

1. Setup qPCR reactions, for both the sgRNA and the 16s loading control, in 
   triplicate.  Make sure to use a plate and seal that are compatible with your qPCR 
   machine.

   I made separate master mixes for each pair of primers I was using (15/77, 
   15/74+, and 16s)::

                                     15/77  15/74+     16s
      Reagent        Conc     Each  42x MM  14x MM  56x MM
      ────────────────────────────────────────────────────
      water                 7.0 μL  294 µL   98 μL  392 µL
      cDNA*                 3.0 μL
      primer mix    10 µM   2.5 μL   35 µL   35 µL  140 µL
      polymerase**     2x  12.5 μL  525 µL  175 μL  700 µL
      ────────────────────────────────────────────────────
                           25.0 μL             22.0 μL/rxn

   \*Unknown concentration because sample was not purified and contains RNA, 
   DNA, and nucleotides.  \**Power SYBR Green PCR master mix (Applied 
   Biosystems 4367659).

2. Run qPCR with the following thermocycler schedule:

   - 95°C for 10 min
   - 40 cycles:
      - 95°C for 15 sec
      - 60°C for 60 sec

.. figure:: 20181002_sgrna_qpcr_curves.svg

   Left panels: Plots showing the progress of the PCR reaction, as monitored by 
   the fluorescence of Sybr Green.  I'm not sure exactly what Rn represents.  
   Right panels: Plots showing the derivatives of the melting curves for each 
   reaction.  Multi-modal curves are indicative of off-target amplification.  
   Blue lines: Weak promoter (J23150).  Red lines: Strong promoter (J23119).  
   Grey dashed lines: Loading control (16S rRNA).

Confirm mhf/30 sequence
-----------------------
Tanja was worried that the mhf/30 had acquired some weird insertions or 
deletions because the gel checking the primers showed so many clean bands of 
the wrong size.  So I sent both g1/mhf/30 and j23150:g1/mhf/30 for sequencing.  
Both came back correct.


Results
=======

.. figure:: 20181002_sgrna_qpcr_ct.svg

   Upper panel: The difference in the number of PCR cycles needed to reach the 
   fluorescence threshold (Ct), compared to the 16s loading control.  Lower 
   panel: Fold-change in sgRNA expression, relative to `j23150 on (apo)`.

- I don't think the mhf/30 primers worked very well.

- I don't really trust the fold changes.  The 2**Ct calculation seems too 
  heuristic.  Once I get the primer standard curves, I think I can use them to 
  make an empirical mapping from ΔCt to fold change.
