***************************
Test ligRNAs in B. subtilis
***************************

We make the claim in the paper that our system may be useful in bacteria 
without facile genetic controls.  The reviewers asked that we back up this 
claim by testing in a bacterial species other than E. coli.  We chose B.  
subtilis (Bs) because it is a model organism and the Carol Gross lab has agreed 
to help get me off the ground with it.  But it's also a good choice because 
it's a gram-positive species, while E. coli (Ec) is gram-negative, so the two 
species are often assumed to be representative of bacteria as a whole (even 
though our collaborators is the Gross lab caution that this is probably less 
true than it seems).

Methods
=======

Tips
----
- B. subtilis grows in LB at 37°C.

- Don't store plates at 4°C.  This "cold shock" causes B. subtilis to 
  sporulate.

- Don't keep B. subtilis in PBS for more than ~30 minutes before doing flow 
  cytometry.  This will also cause B. subtilis to sporulate.  If it's necessary 
  to keep B. subtilis in PBS for an extended amount of time, the cells can be 
  fixed with formaldehyde.

- Use 100 μg/mL to seelct for the sgRNA insert (stock: 100 mg/mL in water, 
  stored at 4°C).  This is probably not strictly 
  necessary, since the gene is genomically integrated, but I like having some 
  antibiotic in there.

- The sgRNA and GFP are driven by the "veg" promoter, `which is 
  constitutive`__.  dCas9 is driven by the xylA promoter, which is induced with 
  1% xylose (stock: 20%).
  
  __ http://parts.igem.org/Promoters/Catalog/B._subtilis/Constitutive

- Looks like I can use up to 8 mM theophylline [Cui2016]_.

Cloning
-------
The Gross lab has a B. subtilis strain that expresses the exact same 
super-folder GFP sequence that I've been using in bacteria.  That's convenient 
for me, because it allows us to use the same guides as before.  I'll begin by 
just using g1 (g2 doesn't seem to work very well).  If I have problems, I can 
come back and think more about which guides I want to use.

I got a B. subtilis sgRNA plasmid from the Gross lab.  I'm going to clone my 
ligRNAs using gBlocks and restriction cloning.  Unfortunately the MCS on this 
plasmid kinda sucks.  All the restriction sites that are present 5' of the 
sgRNA are also present 3' of it, so I have no option but to use the same 
restriction site on both sides of the insert.  This means that I'll get 
fragments inserted in both directions, so I'll have to pick extra colonies to 
account for that.  I decided to use HindIII, since it will allow me to order 
the smallest gBlocks.

It's worth noting that I decided against using inverse PCR because I would've 
had to do three reactions: one to install the spacer, one to install the Dang 
scaffold, and one to install the specific designs.  I could've also just 
ordered one gBlock (e.g. g1/on) and used inverse PCR to clone the designs, but 
ordering all the gBlocks will be the fastest way to make these constructs, and 
I think that's the most important consideration.

:download:`gblocks.xlsx`

2018/06/27:

- Miniprep pJMP3 (the backbone).  Yield: 269.2 ng/µL.

2018/06/28:

.. literalinclude:: restriction_cloning.txt

.. note::

   The above reaction has 10 U of HindIII, which is what was recommended by 
   NEB.  Since I don't often do restriction digests, I wanted to do a quick 
   calculation to make sure that 10 U would be enough:

   - `1 U of HindIII-HF digests 1 µg of λ DNA in 1h at 37°C 
     <https://www.neb.com/products/R3104-HindIII-HF#Product%20Information>`_

   - λ DNA is `48,502 bp long <http://www.bioinformatics.nl/molbi/SCLResources/lambda.htm>`_ and has 
     `6 HindIII sites <http://www.bioinformatics.nl/molbi/SCLResources/LambdaBE_restrct_alphab.htm>`_.

   - My backbone is 7263 bp and has 2 HindIII sites.  

   - (1 µg pJMP3) × (N bp / 1 μg) × (2 HindIII sites / 7263 bp pJMP3) × 
     (48,502 bp λ DNA / 6 HindIII sites) × (1 µg λ DNA / N bp) × (1 U at 
     37°C for 1h / 1 μg λ DNA) = 2.23 U at 37°C for 1h.

   10 U should be plenty.

If I have trouble with this, order primers to linearize the backbone and do 
Gibson.  Or order BsrGI and PmeI, but primers would be cheaper.  Why didn't I 
just think to do Gibson in the first place?

Transformation
--------------
2018/07/17:

Cameron in the Gross lab did most of this, but I watched.  The protocol is 
pretty simple: grow the cells to a particular OD in a minimal media; add 100 ng 
DNA; incubate at 37 for 2h; plate.

Once Cameron sends me the protocol we used, I'll fill in the details here.

We transformed g1/on, g1/off, g1/rxb/11/1, and g1/mhf/30 into the 371 strain, 
which has dCas9 and sfGFP.

Theophylline toxicity
---------------------
2018/07/18:

- I meant to do the titration starting at 4 mM theophylline, but I went into 
  auto-pilot and just prepared 1 mM theophylline instead.

- I did not observe any toxicity up to 1 mM theophylline.

.. figure:: 20180720_theo_growth_curve_od600.png

    Growth curves (OD600 vs time).  In color are the replicates for the sgRNA 
    and theophylline concentration corresponding to each plot.  In grey are all 
    the other curves, for comparison.  Plus marks indicate the measurments 
    recorded by the plate reader.  Solid lines are the exponential fit to the 
    circled data points (which are those with OD < 0.08).

.. figure:: 20180720_theo_growth_curve_t12.svg
    :width: 400 px

    Parameters of the exponential fits displayed in the above panel, for 
    easier comparison.  The exponential model is as follows: 
    :math:`A * 2^{t / B} + C`, where A, B, and C are shown in the top, middle, 
    and bottom panels.  Note that this model does not explicitly consider lag 
    time, but models that do (that I tried) produced poor fits.  Also note that 
    the parameters don't make sense if interpreted strictly.  The real initial 
    OD is (a) the same for every culture and (b) much greater than 1e-5.  I 
    think that the "Initial OD" and "Blank error" parameters collectively 
    represent some sort of lag time.

.. figure:: 20180720_theo_growth_curve_gfp.svg

    Fluorescence signals over time.  The lines are colored by the concentration 
    of theophylline.

Givn the complete lack of toxicity, I became a little worried that theophylline 
couldn't get into gram-positive cells, so I looked for other examples of people 
using theophylline in B.  subtilis.  There are many.  Cui2016_ recommended 4 mM 
theophylline, but also reported a greater effect-size with 8 mM.  Maybe 
theophylline is just not as toxic to B. subtilis, in which case this could be a 
great opportunity to extend that in vivo titration out to higher 
concentrations.  I'm going to try repeating this growth curve up to 16 mM 
theophylline, to see if I can see a growth defect.

2018/07/21:

I repeated the titration, going to very high concentrations of theophylline and 
including the ligRNAs to get an initial idea of how they work.

- There seems to be no toxicity at or below 2 mM theophylline.  Even above 
  that, the toxicity seems limited to a longer lag time with only a slight 
  effect on the doubling time.

- mhf/30 is working as intended, although it seems to require much higher 
  concentrations of theophylline than it did in E. coli.  rxb/11/1 does not 
  seem to be functional, although I still want to do flow.  

.. figure:: 20180721_theo_growth_curve_od600.png

    Growth curves (OD600 vs time).  See above for description.

.. figure:: 20180721_theo_growth_curve_t12.svg
    :width: 400 px

    Parameters of the growth curve exponential fits.  See above for 
    description.

.. figure:: 20180721_theo_growth_curve_gfp.svg

    Fluorescence signals over time.  See above for description.
    
Flow cytometry
--------------
2018/07/25:

I'm going to use 2 mM theophylline for this experiment.  That wasn't enough to 
get much of a signal in the plate reader experiments, but it was the most I 
could use without seeing toxicity, and I hoping that the flow cytometer might 
be more sensitive.

- Make overnight cultures for g1/on, g1/off, g1/rxb/11/1, and g1/mhf/30.

- Start day cultures:

  - Master media:
    - 12 mL LB
    - 600 µL xylose
    - 12 µL spec

  - apo media:
    - 5 mL master media
    - 333 µL LB

  - holo media:
    - 5 mL master media
    - 333 µL 30 mM theo in LB

  - Inoculate 1 mL cultures with 4 µL overnight.

- Grow at 37°C for 8h.

- Dilute 0.5 µL day culture into 250 µL PBS

- Measure fluorescence by flow cytometry.

.. figure:: 20180725_test_b_subtilis.svg

    ligRNAs targeting GFP in B subtilis, with and without 2 mM theophylline.

- The difference between the controls is good: 100x.

- Both ligRNAs are functional, although their signals are weak (<2x).

- It's worth noting that both ligRNAs were more fluorescent than the negative 
  control in the "expressing" state, although only by a little bit.  Still, 
  that shouldn't be the case.

- ligRNA⁻ is almost fully active in the *absence* of ligand, so adding more 
  ligand will not help any.  There's just not enough active Cas9 in the cell.  
  I should ask Jason what I can do to get greater Cas9 and/or sgRNA expression.

- My plate reader results suggest that I can make ligRNA⁺ at least a little 
  better by simply adding more theophylline.  I'm going to try that tomorrow, 
  to at least know what the upper limit on ligRNA⁺ function is in this setup.

2018/07/31:

I want to test 8 mM theophylline, to see if I can get better ligRNA⁺ activity.  
I decided to titrate down to 4 mM and 2 mM as well, just to be more thorough.

- Make overnight cultures for g1/on, g1/off, g1/rxb/11/1, and g1/mhf/30.

- Prepare apo and holo media

  - 26 mL Master Mix
    - (6.93 µL media/ligand)
    - 1.3 mL 20% xylose
    - 26 µL spectinomycin
    - 17.74 mL LB

  - 14 mL apo media
    - 3.73 mL LB
    - 10.27 mL master mix

  - 10 mL holo media
    - 2.67 mL 30 mM theophylline (in LB)
    - 7.33 mL master mix

- Inoculate each 1 mL culture with 4 µL overnight.

- Grow at 37°C for 8h.

- Dilute 0.5 µL day culture into 250 µL PBS

- Measure fluorescence by flow cytometry.

Comments

- As expected, increasing the concentration of theophylline does not improve 
  ligRNA⁻, as it is almost fully expressing even in the absence theophylline.

- 8 mM theophylline only results in a 2.77x fold change.  
  
Results
=======

.. figure:: 20180731_b_subtilis_theo_titration.svg

    ligRNAs targeting GFP in B subtilis. Solid lines are with theophylline, 
    either at 8 mM, 4 mM, or 2 mM (see y-axis label).  Dashed lines are without 
    theophylline.

I don't think either ligRNA is good enough to publish.  

..
   I asked the Gross lab if Cas9 expression could be increased by increasing 
   xylose, and they pointed me to I could try increasing Cas9 expression by 
   using a constitutive 

.. 
   My two options, if I don't want to abandon this system completely, are to 
   try a weaker GFP promoter or a constitutive Cas9 promoter.  In either case, 
   I'll have to ask the Gross lab for a bunch of plasmids and strains.

References
==========

.. [Cui2016] :doi:`10.1186/s12934-016-0599-z`
