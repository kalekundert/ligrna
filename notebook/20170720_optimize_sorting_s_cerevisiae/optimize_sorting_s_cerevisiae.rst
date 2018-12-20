******************************
Optimize sorting S. cerevisiae
******************************

Before I can actually screen a library in yeast, I need to determine how well I 
can sort a mixture of the two controls.  I'm worried in particular about the 
lack of separation between the populations.  The modes of the two control 
populations are separated by 15x--20x, but the breadth of the distributions 
seems a little wider than that.  As a result, the populations overlap to some 
extent.  I think I'll be able to draw gates that only include one population or 
the other, but I want to be sure.

.. figure:: 20170720_venus_controls.svg
   :align: center

I also want to establish some parameters much as I did with bacteria:

- How fast can I go?
- How many cells survive sorting?
- Which ODs correspond to which sorting efficiencies?

Protocol
========
The cells I used for this experiment had grown for 24h as part of "Try #7" in 
:doc:`/20170510_run_tdh1_controls/run_tdh1_controls`.

1. Measure the OD600 of the tdh1/on and tdh1/off cultures:

   .. od::
      :dilution: 20x

      tdh1 on:  0.5248
      tdh1 off: 0.5205
      
2. Record 1:100 dilutions (i.e. OD≈0.1) of both controls on the FACSAria II.  

3. Tune the lasers such that the cells stay within the dynamic range of the 
   cytometer:

   =======  =======
   Channel  Voltage
   =======  =======
   SSC      236V
   FSC      88V
   FITC     478V
   =======  =======

4. Decide which dilutions to test.  The 1:100 dilutions I recorded initially 
   had event rates of about ≈900 evt/sec.  Based on this, I chose the following 
   dilutions:

   ========  =================  ===============  ======================
   Dilution  Volume cells (μL)  Volume PBS (μL)  Event rate (estimated)
   ========  =================  ===============  ======================
      1:5                  200              800                  20,000
      1:10                 100              900                  10,000
      1:33                  30              970                   3,000
      1:100                 10              990                   1,000
   ========  =================  ===============  ======================

   I didn't want to run the risk of clogging the machine by using undiluted 
   cells (or even not-very-diluted cells; 1:5 was definitely pushing it).  But 
   I also wanted to reach an event rate of 20,000 evt/sec, since that it the 
   most efficient speed for sorting bacteria.

5. Draw gates for the on and off populations.

   Unlike with bacteria, these two populations overlap.  I don't know how I'll 
   draw gates for the screen, but for this experiment I thought it made sense 
   to draw the gates to fit as much of the target population as possible 
   without overlapping the other population at all.

   - Make an gate for live cells.  I did this by making an auto-polygon gate 
     around the control populations in the FSC vs. SSC plot.

   - Make gates for each population.  I did this by making an auto-polygon gate 
     around each population, then manually adjusting it until there was no 
     overlap with the other population.  The "off" gate ended up pretty oval, 
     while the "on" gate ended up oval with a big chunk missing.

6. Prepare 1:99 and 99:1 mixtures of the on and off controls, then dilute them 
   to the levels chosen above.

   =============  =======  ========
   Mixture        on (μL)  off (μL)
   =============  =======  ========
   1% on (1:99)         4       396
   1% off (99:1)      396         4
   =============  =======  ========

7. Sort the cells.  Record the populations before and after each sort, and make 
   note of all the sort parameters.

   - Create "tubes" for the before and after populations in FACSDiva.
   - Put a clean tube in the collection chamber.
   - Make sure the flow rate is set to "1".
   - Transfer cells to sample tube, then vortex and load.
   - Record the before population.
   - Start sorting.  Collect at least 2000 events, or 5000 if 2000 didn't take 
     too long.
   - Stop sorting and discard the sample tube.
   - Add ≈500 uL of PBS to the collection tube from the stream.
   - Gently roll the liquid around the tube to get all the droplets.  *Do not 
     vortex!*  The cells are too fragile now, and vortexing destroys them.  I 
     know this because I vortexed the first three samples, and they all had 
     really screwy-looking FSC/SSC plots afterwards.  Then I tried not 
     vortexing, and the FSC/SSC plot looked exactly as it did for the unsorted 
     cells.
   - Load the collection tube and start recording the after population.  Turn 
     the flow rate up to "11".
   - While that's going, export the sort report to CSV and copy the relevant 
     information into a spreadsheet.
   - Unload and discard the collection tube once >1000 events have been 
     recorded.
   - Copy the statistics for the before and after populations into the 
     spreadsheet.

8. Plate the sorted cells to determine what fraction remain viable after 
   sorting.  I plated both on cells (sorted from 1:10 dilution of the "1% on" 
   mixture) and off cells (sorted from the 1:10 dilution of the "1% off" 
   mixture) on YPD plates to make sure neither population was more or less 
   likely to survive, and I plated on cells (from the same mixture as before) 
   on a -LEU and a -HIS plate to see whether the selective pressure reduces 
   survival.  (I would've used a -LEU -HIS plate, but I don't have the 
   necessary reagents yet.)

   - Pre-warm the plates at 30°C.  

   - Sort 2000 cells into 1 mL of YPD.

   - Invert to mix a few times.

   - Plate 100 uL.

   - Incubate at 30°C for 2-3 days.

   - Count the colonies on each plate.

   ==========  =======  ========  ======  ==========  ==========
   Population  Mixture  Dilution  Plate   # Colonies  % Survival
   ==========  =======  ========  ======  ==========  ==========
   on          1% on    1:10      YPD             92          46
   off         1% off   1:10      YPD             84          42
   on          1% on    1:10      SD-Leu          93          47
   on          1% on    1:10      SD-His         112          56
   ==========  =======  ========  ======  ==========  ==========

Results
=======
The spreadsheet containing the population statistics and the sorting parameters 
can be downloaded here:

:download:`./optimize_facs_for_yeast.gnumeric`

