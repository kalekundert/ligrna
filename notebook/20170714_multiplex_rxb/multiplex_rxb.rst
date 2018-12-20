******************
Multiplex rxb 11,1
******************

The data from the initial multiplexing experiment were not very striking.

.. figure:: multiplexing_data.svg
   :align: center

The `apo` data looks good, but it's not at all clear that the system is 
responding as it should to the two ligands.  One problem was that the `3mx mhf` 
sensors (both 30 and 37) have fairly significant responses to theophylline:

.. figure:: 3mx_fold_change_matrix.svg
   :align: center
   :width: 400

I don't know why the `3mx` aptamer would be more specific in the context of the 
`rxb` sensors than the `mhf` ones, but that seems to be the case.  Given this, 
the multiplexing experiment will probably be much more striking if done using 
`rxb 11` for both guides, e.g. `gfp theo rxb 11,1` and `rfp2 3mx rxb 11,1`.

I also think that the experiment will be easier to understand if done like 
this.  As it is, the experiment is always hard to wrap your mind around because 
the two reporters are being regulated in different directions (i.e. forwards vs 
backward).  With just `rxb 11,1`, the two reporters will be regulated in the 
same direction.  They'll also be turned on by ligand, which should be even more 
intuitive.

I had to decide between using `gfp/theo` with `rfp2/3mx` or `gfp/3mx` with 
`rfp2/theo`.  The decision was pretty arbitrary, but I decided to use 
`gfp/theo` with `rfp2/3mx` because `gfp/theo` has the highest fold change of 
any of my constructs.  It's not by a lot, but I figured it would be better to 
include that construct than to exclude it.

I also decided that it would be better to use multiplexed controls rather than 
the usual controls for this experiment.

I'm planning to do this experiment in two parts.  First, in what I'm calling 
the "ligand matrix" experiment, I'm just going to test the 4 combinations of 
theo and 3mx on their own (i.e.  individual cultures with either no ligand, 
just theo, just 3mx, or theo and 3mx) to make sure the multiplexed constructs 
behave like they should.  Second, in what I'm calling the "time course" 
experiment, I'm going to test periodically (i.e. every 8h) exchanging the media 
for a single culture.  The time course experiment is what I really want to 
include in the paper, but it's very challenging to do, so I want to be sure 
it'll work before starting on it.

Methods
=======

Cloning
-------
The specific templates I used for each inverse PCR reaction were:

=========  =================  =================
Construct  Backbone Template  Insert template
=========  =================  =================
pKBK007    gfp theo rxb 11,1  rfp2 3mx rxb 11,1
pKBK009    gfp on             rfp2 on
pKBK010    gfp off            rfp2 off
=========  =================  =================

The primers I used for the backbone and insert reactions were:

=========  =======================================  =======================================
Reactions  Forward Primer                           Reverse Primer
=========  =======================================  =======================================
Backbone   MULTIPLEX_BACKBONE_TM73_FOR              MULTIPLEX_BACKBONE_TM71_REV
Insert     sgRNA_Transcriptional_Unit-Forward-CORR  sgRNA_Transcriptional_Unit-Reverse-CORR
=========  =======================================  =======================================

I used an annealing temperature of 72°C for the backbone templates, and a 
temperature of 62°C for the insert templates, and I actually did 35 cycles, 
despite what the protocol says.

.. literalinclude:: 20170822_pcr.txt

.. literalinclude:: 20170822_golden_gate.txt

Ligand matrix --- Aug 24, 2017
------------------------------
I prepared 3.12 mL of media for each condition using the following recipe.  For 
5 conditions, this requires 8 mL (4 aliquots) of 2x EZ media.  I mixed all the 
2x EZ aliquots together in one tube to make sure each condition got the same 
media:

=========  =====  ===========
Reagent    Conc   Volume (μL)
=========  =====  ===========
EZ media   2x            1560
ligand #1  30 mM          104
ligand #2  30 mM          104
water                    1352
=========  =====  ===========

I had to change the thresholds I was using on the LSRII, because I'm now 
interested in cells that are fluorescent in neither the RFP nor the GFP 
channel.  So I set very permissive thresholds for the SSC (threshold=200) and 
FSC (threshold=200) channels (both thresholds were as low and FACSDiva would 
let them go).  I then drew an auto-polygon gate around the cluster of cells in 
FSC/SSC space, and only considered events in that gate.  I found that 
normalizing the data by SSC-A gives slightly tighter distributions than 
normalizing by either nothing or FSC-A.

.. literalinclude:: 20170825_crispri_assay.txt

Time course --- Aug 31--Sep 2, 2017
-----------------------------------
We decided to use new plates each day, to reduce the chance of contamination.

The flow cytometry after the first night didn't work because we were 
thresholding on the fluorescent channels, but some of the cells in this 
experiment aren't fluorescent.  I'd dealt with this problem before and had an 
experiment template that gates on FSC vs SSC instead, but James didn't know 
about it.  He tried adding more cells (because the counts were low) but of 
course that didn't help.  Ultimately he gave up and put the cells back at 4°C, 
and I reran the plate in the morning.

.. literalinclude:: 20171005_crispri_multiplex_timecourse.txt

Results
=======

Ligand matrix --- Aug 24--27, 2017
----------------------------------
The traces were very consistent for all three replicates.  I found that 
normalizing the data by SSC improved the sharpness of the peaks.  I'm 
considering normalizing all of the my other data by SSC rather than the 
constitutive fluorescent channel, because it seems to work well and it would be 
more consistent.

.. figure:: 20170824_multiplex_controls_traces.svg

The theophylline aptamer is about 2x less responsive to 3mx than it is to theo.  
This result is consistent with the data James collected:

.. figure:: 20170824_multiplex_controls.svg

The decision I have to make is whether to use 3mx or theo+3mx in the time 
course.  The following two plots are mockups of what I expect the time course 
data to look at, made by just plotting the ligand matrix data in a different 
order (and duplicating some of it, too).  The time labels are bogus.  

If I alternate between theo and 3mx (a), both channels respond to the ligand, 
but the GFP response is weak.  That's expected, because 3mx partially activated 
the theo aptamer, but I worry that it makes the data look weaker.

On the other hand, if I alternate between theo and theo+3mx (b), the GFP 
channel stays fully off and only the RFP channel responds to the 3mx.  This 
makes the responses look very binary, but also makes it look like the GFP 
channel doesn't really respond to ligand.

.. figure:: 20170828_mockup_multiplex_time_course.svg
   :align: center
   :scale: 50%

Time course --- Aug 31--Sep 2, 2017
-----------------------------------
The time course data is very consistent with the ligand matrix data.  The only 
thing that bothers me (and I didn't notice this with the ligand matrix 
experiment) is that the gfp and rfp constructs have noticeably different fold 
changes.  From James' ligand matrix data, I expected them to be more similar 
(about 10x each, rather than ≈15x and ≈7x).  I wonder if I would've gotten a 
stronger rfp2 signal if I'd made the 3mx fresh.  Still, the data is 
high-quality and makes the point I want to make, so I think it's fine.

.. figure:: 20170831_multiplex_time_course_theo_3mx.svg
   :align: center


Troubleshooting
===============

Primers too old
---------------
James used Golden Gate assembly to make the first multiplexed construct.  More 
specifically, he used PCR to linearize the backbone of one pBLO plasmid (with 
the guide included) and to add BsmBI sites to either end.  He then used PCR to 
amplify the second guide from another pBLO plasmids and to add complementary 
BsmBI sites.  The primers are not at all dependent on the particular guides 
being cloned, so I just used the same ones as James.

========================================  ============================  ====================================
James' Name                               Kale's Name                   Sequence
========================================  ============================  ====================================
Linear_MS2_sgRNA_Vector-Forward           MULTIPLEX_BACKBONE_TM_72_FOR  gtccacgtctcaagcatttccataggctccgccccc
Linear_MS2_sgRNA_Vector-Reverse           MULTIPLEX_BACKBONE_TM_72_REV  taccacgtctcatcagaacgccagcaacgcgg
sgRNA_Transcriptional_Unit-Forward-CORR   MULTIPLEX_INSERT_TM_69_FOR    taccacgtctcactgaTTGACAGCTAGCTCAGTCCTAGGT
sgRNA_Transcriptional_Unit-Reverse-CORR   MULTIPLEX_INSERT_TM_69_REV    gtccacgtctcatgctGTTCACCGACAAACAACAGATAAAACGAAAG
========================================  ============================  ====================================

James had a lot of trouble building this construct because he initially ordered 
the wrong primers, so I carefully double-checked these to make sure they were 
in fact the right primers.  I transcribed the sequences off the primer tubes, 
then used those sequences to do a simulated Golden Gate reaction in SnapGene.  
Everything seemed to check out, so I went ahead with the reactions.

When I tried to use James' backbone linearization primers, I found that the 
tubes were empty.  I thought this was probably due to evaporation, so I tried 
to redissolve any primers still in the tube by adding 50 μL EB to each tube, 
mixing vigorously by pipetting and vortexing, and incubating at 50°C for a few 
minutes.  (I was loosely following the protocol IDT gives you for resuspending 
their lyophilized DNA.)

When I setup the PCR, I diluted the primers as if they were still 200 μM.  The 
PCR ultimately worked, but the product band was very faint compared to the 
transcriptional unit reaction.  If I use these primers again, I probably 
shouldn't dilute them as much.

I also realized after I setup the PCR that the melting temperatures 
predicted by NEB's online calculator were much higher that the temperatures 
James gave me: 72°C instead of 62°C for the backbone primers, and 69°C 
instead of 60°C for the insert primers.  That said, the reaction seemed to 
work fine at 60°C.  The backbone band was faint, but I think that was more 
likely due to the primer concentration, as discussed above.  I didn't see 
any off-target bands.

For the golden gate reaction, I use the following thermocycler protocol:

1. 42°C for 5 min (for the restriction enzyme).
2. 16°C for 5 min (for the ligase).
3. Back to step 1 4 times.
4. 55°C for 5 min.

There are two things worth noting about this protocol.  The first is the 
restriction enzyme temperature.  I was using BsmBI, which NEB recommends 
using at 55°C.  In contrast, NEB recommends 37°C for most other golden gate 
enzymes, including BsaI, which is the most common Golden Gate enzyme.  I was 
worried that the thermocycler protocols I was finding online were intended 
for BsaI, and that I should increase the temperature for BsmBI.  However, 
the heat inactivation temperature for T4 ligase is 65°C, and I was also 
worried that 55°C was a little too close to that.  I ended up using 42°C as 
recommended here: 

http://barricklab.org/twiki/bin/view/Lab/ProtocolsGoldenGateAssembly

The second thing worth noting is the number of cycles.  Most protocols I 
found online recommended doing 30, but Anum told me earlier that she uses a 
1h protocol for single inserts.  I couldn't find her exact protocol, but I 
also didn't have 5h to kill, so I just reduced the number of cycles such that 
the whole protocol took just under 1h.  [KBK: I later talked to Anum, and she 
told me that her 1h protocol still does 30 cycles, it just spends less time 
(90s) on each cycle.]

When the reaction was done, I did a transformation using 100 μL Top10 cells 
and all 10 μL of the Golden Gate reaction.  Anum told me that she usually 
transforms the whole reaction, but I forgot to ask her many competent cells 
she uses.  I decided to use 100 μL (which is *a lot*) because the backbone 
PCR didn't work very well and I was worried about not getting very many 
transformants.

I tried the Golden gate reaction twice.  The first time, I got plenty of 
colonies, but the all were missing the insert.  The second time, I only got two 
colonies.  One had no insert, and the other had the insert twice.

I think the problem is that the backbone PCR isn't working very well.  The 
primers have a very high Tm (72°C), which I confirmed with a gradient PCR 
(kind-of, I only went to 68°C with the gradient, but that was the best Tm).  To 
try to optimize the reaction, I designed new primers with a lower Tm.  Of 
course, these primers ended up very short because they bind a region that is 
≈70% GC.  I also reordered James' primers, because the evaporated and rediluted 
primers that had been left at room temperature for months could have easily 
been causing problems on their own.

.. figure:: 20170802_pcr_multiplexing_fragments.svg

Both sets of fresh primers worked better than the old ones (not shown above), 
but the primers with the higher Tm (i.e. the primers with the same sequence 
that James designed) were more specific.  The insert PCR continued to work well 
at Ta=62°C.  I discarded James' old primers and put my new ones in the freezer, 
for future use.

Forgot theo+3mx condition --- Aug 24, 2017
------------------------------------------
The first time I did the ligand matrix experiment, I forgot to include the 
condition with theo and 3mx.  Other than that, the data looked really good.


