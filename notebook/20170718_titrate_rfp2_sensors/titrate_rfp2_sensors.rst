********************
Titrate rfp2 sensors
********************

I decided to repeat the :doc:`in vivo titration experiment 
</20170323_titrate_candidate_sensors/titrate_candidate_sensors>` using `rfp2`, 
because I think it's important to do the validation experiments with a spacer 
that was not part of the original screen.  

Methods
=======
I used EZ media and incubated with shaking at 225 rpm.  On different days I 
grew the bacteria for slightly different amounts of time:

===========  ===========
Replicate    Growth time
===========  ===========
Aug 7, 2017         8h50
Aug 8, 2017         9h00
Aug 9, 2017         9h00
===========  ===========

.. literalinclude:: ./20170808_crispri_titration.txt

Results
=======
.. figure:: 20170807_titrate_rfp2.svg
   
Troubleshooting
===============

Noisy data --- July 18, 2017
----------------------------
The data I collected for the first replicate was too noisy to be of publication 
quality (which is the whole purpose of this experiment).  The controls are 
particularly bad.  It's also worth noting how close all the sensors get to the 
`off` control.  `rxb 11` even goes just above it at the end.  This is 
suspicious because in previous experiments the `rfp2` sensors have always been 
more in the middle of the dynamic range.

.. figure:: 20170718_titrate_rfp2.svg

No response to ligand -- July 19, 2017
---------------------------------------
I only had enough media to do this experiment once, so I made new media for the 
second and third replicates.  However, none of the designs in the second 
replicate showed any response to theophylline.  This made me think that maybe I 
made a mistake making the media (did I forget to add the ligand?!) or that my 
theophylline stock had gone bad, although I could've also just made a mistake 
setting up the titration.

.. figure:: 20170719_titrate_rfp2.svg

To figure out what happened, I setup an experiment with media from the batch I 
used in the first replicate, media from the batch I used in the second 
replicate, and media that I prepared on the day-of from frozen 2x EZCCA and my 
theophylline stock (500 μL 2x EZ, 33.3 μL 30 mM theophylline, 467.7 μL water).  
I grew rxb 11,1 (but not either of the controls) in each media for 9h, then 
analyzed the populations by flow cytometry.

.. figure:: 20170720_test_new_media.svg

All three media performed well, so that was not the problem.  I must have just 
messed up the serial dilution.

Left the plastic cover on --- Aug 4, 2017
-----------------------------------------
I decided to try growing the cells in LB rather than EZ media.  When I was 
initially testing the *in vivo* assay in 96-well blocks, I found that some 
designs worked better in LB than in EZ, although both media worked well in 
culture tubes.  I also can't remember which media I used for 
:expt:`20170323_titrate_candidate_sensors`, but I know I used LB to test 
individual clones from my screens in 96-well blocks.

I screwed up the initial experiment by leaving the plastic cover on the plate, 
so the cells weren't getting enough oxygen.  I also realized after-the-fact 
that I forgot to add ATC to the media, so Cas9 wasn't induced either.  In the 
end, the cells were sharply bimodal and the response to ligand was weak.

.. figure:: 20170804_titrate_rfp2.svg

Poor growth in LB --- Aug 5, 2017
---------------------------------
I repeated the LB experiment from yesterday, but this time I noticed that I 
didn't get even growth across the plate.  Columns 1-3 grew pretty well, while 
columns 4-12 grew very poorly.  I'd be surprised if this was related to the 
ligand, because that would mean the cells grew best with theophylline!  More 
likely, this had to do with some wort of temperature gradient or shaking issue.  

The figure shows the event rates measured on the flow cytometer for the `on` 
wells.  As usual, I diluted 0.5 μL of cells into 250 μL PBS, and set the flow 
rate to 0.5 μL/sec.  The rest of the wells in this experiment have more normal 
event rates, because I added more 3x more cells and turned the flow rate up 4x.

.. figure:: 20170805_titrate_rfp2.svg

24-well blocks -- Aug 7, 2017
-----------------------------
Considering the noisiness and poor growth of some of the previous experiments, 
I thought I might get more consistent data by growing the cells in a 24-well 
block.  I went back to using EZ media for this experiment, since I've never had 
any problems with it in the larger-volume format.  This worked really well, and 
I got data that looked just as good as the `gfp` experiment (see `Results`_ 
below).

Looking back, I probably used 24-well blocks for the `gfp` experiment as well.  
Let this be a lesson as to why I should write shit down!  I could've saved two 
weeks and a bunch of late nights just by doing the same protocol I'd already 
worked out!

Large error bars --- Aug 9, 2017
--------------------------------
The first two replicates agreed very well with each other, but the third one 
was shifted a little such that the overall dynamic range was the same, but the 
error bars on the titration curves became much larger.  I'm not sure whether or 
not I should discard the third replicate.  On one hand, it's definitely wrong 
to discard data just to make the error bars look better.  On the other hand, 
the data aren't really as noisy as the error bars make them look.  The actual 
titrations are pretty similar, each experiment just seems to have a different 
baseline level of RFP fluorescence relative to GFP.

Having written this out, it occurs to me that I should just normalize the 
fluorescence values for each titration relative to the value of the 
corresponding `off` control.  I was initially hesitant to do this because in 
general I agree with Tanja that the less data is normalized, the better.  In 
this case, though, the normalization removes an effect that's not important to 
the point I'm trying to make and allows the actual variance in sensor activity 
to be much more clearly presented.  I think that justifies the cost of making 
the data more abstract.


