****************
Understand w11,1
****************

In :expt:`20170227_test_m11_w11_sensors`, I was surprised that `w11 1` was 
constitutively off.  Because this observation doesn't fit with our proposed 
mechanism, I want to look into it more closely.

Confirm result
==============
To confirm that the initial result wasn't a mistake, I repeated the flow 
cytometry experiment.  I also sequenced the MG1655 cells directly to confirm 
that I had actually transformed the right construct and that I hadn't made any 
mistakes cloning.

I was somewhat *ad hoc* about this experiment.  I retested ``w11 1`` twice.  
The first time, I didn't make an overnight; I just suspended a colony in 20 μL 
EB and used 4 μL each to inoculate the apo and holo media.  I sent the 
remaining 12 μL of cells directly for sequencing.  After the flow cytometry 
experiment, I also inoculated 4 mL LB with 0.5 μL cells from the day culture, 
to miniprep and sequence.

The second time, I made a 3 mL ``w11 1`` overnight culture.  I started a flow 
cytometry experiment from the overnight culture, then I miniprepped the rest to 
send for sequencing.

I got the same results as before in both flow cytometry experiments:

.. figure:: 20170420_repeat_w11_1.svg
    :width: 400 px

All three colonies I sent for sequencing came back with the expected ``w11 1`` 
sequence:

.. figure:: w11_1_sequencing.png

Mutational analysis
===================
There are two questions I can think to ask at the moment:

1. Do ``w11 1,a`` and ``w11 1,u`` work?  Instead of strand-swapping the GC base 
   pair at the bottom of the nexus, these mutants replace it with AU and UA 
   pairs.  Briner14_ showed that, in the context of the "wildtype" sgRNA, an AU 
   pair works well at that position.

2. Does the GC strand-swap work in the context of the positive control.  I'm 
   calling this construct ``won`` (pronounced "double-you-on").

Here are the primers I ordered for these constructs:

.. command-output:: ../scripts/clone_into_sgrna.py won w11/1/a w11/1/u

I also decided it would be prudent to test ``won a`` and ``won u``:

.. command-output:: ../scripts/clone_into_sgrna.py won/a won/u

I tested each of these constructs using the CRISPRi flow cytometry assay:

.. figure:: 20170502_won_w11_1.svg

For the ``on`` mutants, any base pair seems to work at that position (the 
bottom of the nexus stem).  For the ``rxb 11,1`` mutants, only GC is allowed at 
that position.  Any other base pair renders the guide indistinguishable from 
the negative control.

I cannot think of any reason for such a profound effect.  Hopefully the 
SHAPE-Seq data will help us form a hypothesis.  If not, maybe it'll be worth 
doing SHAPE-Seq on ``w11 1``.

I was just looking at the sequences identified in the ``rxb`` screen, and I 
noticed that 2 of the hits (``rxb 22`` and ``rxb 51``) have a GU base pair at 
the base of the nexus stem (the other 7 had a GC pair).  This suggests two 
things:

1. The G is what's really important.

2. The importance of the G probably doesn't have anything to do with the rest 
   of the evolved stem, because pretty much every other position samples every 
   base in at least one of the hits [1]_. 

I could test ``w11 1,h`` (and ``w11 1,v``, why not) to support this hypothesis. 
   
.. [1] The exception is the top of the stem, which always has a purine on the 
   5' side and a pyrimidine on the 3' side.  This is probably a coincidence 
   though, because I have several ``m11`` and ``w11`` designs that work fine 
   with the purine on the 3' side.  And actually, now that I look at the 
   sequences again, the whole 5' side is biased towards purines.  This might be 
   a cloning artifact. I saw a bias toward A on the 5' side in 
   :doc:`/20170329_test_multiple_spacers/test_multiple_spacers`, and maybe that 
   bias in conjunction with a need to be base-paired could favor sequences like 
   these.

.. [Briner14] Briner et al. Guide RNA functional modules direct Cas9 activity 
   and orthogonality.  Mol Cell (2014) 56:333-339.

