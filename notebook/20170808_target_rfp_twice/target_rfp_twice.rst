****************
Target RFP twice
****************

An obvious question to ask is whether we can get better dynamic range by 
targeting the same gene twice.  We can test this using RFP, since both the 
`rfp` and `rfp2` spacers work well with all the sensors.

Preliminary data
================
I decided to test the `rfp/rfp2 rxb 11,1` construct before I finished cloning 
any of the others, just to see if this idea has any promise.  

.. figure:: 20170808_double_target_rfp.svg

The construct with two sensors does have the best dynamic range, but a few 
things are suspicious about this data.  First, `rfp rxb 11,1` didn't work as 
well as it should have.  Second, the improved dynamic range comes from 
expressing more RFP when theophylline is present.  I would've expected any 
improvements to be due to expressing less RFP when theophylline is absent.  An 
increase in expression is weird, because binding by either sensor should be 
sufficient to suppress RFP.  Still, it's promising, and I think the `rfp on : 
rfp2 on` and `rfp off : rfp2 off` controls will be informative.

Methods
=======
I grew the cells in EZ media in a 24-well block, with shaking at 225 rpm.

I did the first replicate on Aug 26, and the second and third replicates on 
Sept 20-21.  I retransformed the everything for the second and thrid 
replicates.

.. literalinclude:: 20170808_crispri_assay.txt

Results
=======
Ignoring the problems with the rfp controls outlines in the `Troubleshooting`_ 
section, it's not clear that targeting with two guides improves dynamic range.  
It does seem to help for mhf/30, but it doesn't seem to help for mhf/37 (and 
mhf/37 is really the only case where the rfp control worked).  The distribution 
for the double-targeted rxb/11 also has a funny shoulder in all three 
replicates; I'm not sure what that's about.

Given that, I don't think this experiment is worth pursuing any further.

Troubleshooting
===============

rfp constructs don't grow well --- Aug 8, 2017
----------------------------------------------
Most of the data looks good, but rfp/rxb/11/1 has messed-up populations and a 
really poor fold-change.

.. figure:: 20170826_double_target_rfp.svg

What the data doesn't show is that most of the rfp constructs didn't grow well.  
This is probably what's at the root of the poor rxb data point.

.. literalinclude:: 20170921_events_per_sec.txt

I'm not sure how to explain this.  The transformed colonies for all these 
constructs look perfectly healthy, and the overnight cultures grow well.  But 
how well the cultures grow relative to each other is consistent:  mhf/30 is the 
best, the on and off controls are worse, and rxb/11 is the worst.  mhf/37 grows 
fine.

I resequenced rfp/rxb/11/1 to be sure it was correct, and it was.  It seems 
like the problem has to be something specific to the actual constructs, given 
how robust the growth defects are, but I can't imagine what.  It can't be that 
the rfp guide is having an off-target effect on some essential gene, because 
the on and off controls have the same growth defect.  I did have a problem with 
the rfp controls earlier in the project, but I resolved it by retransforming, 
and these experiments were all done with colonies picked from freshly 
transformed plates.  Maybe I should try making new competent cells, or using my 
glycerol stocks of these constructs?

