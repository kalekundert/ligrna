***************************
Optimize BMH139 growth time
***************************

I spent a lot of time optimizing growth conditions for BMH127, ultimately 
settling on a protocol that lasted 24h, with a dilution after 16h.  However, 
that strain was very sick and grew very slowly.  I've continued using the same 
protocol with the much healthier BMH139 strain, but now I want to figure out 
how long this strain needs to grow to get the maximal difference between the 
controls.

Methods
=======
1. Start overnight cultures in 1 mL YPD from freshly-picked colonies of tdh1/on 
   and tdh1/off.

2. In the morning, measure the fluorescence of the overnight cultures by flow 
   cytometry.

2. Prepare 30 mL YPD + estradiol.  I only need 2 mL, but I didn't want to 
   bother serially diluting the estradiol.
   
   - 30 mL YPD
   - 1 μL 3.6 mM estradiol

3. Dilute 5 μL of each overnight culture into 1 mL fresh YPD + estradiol.

4. Incubate the cultures at 30°C with shaking at 225 rpm.

5. Measure the fluorescence of the day cultures by flow cytometry every hour, 
   starting at 7h.

Results
=======
The populations seem to start plateauing around 9h.  I meant to take an 11h 
timepoint, but unfortunately I forgot to put the cells back in the incubator 
after the 10h timepoint.  In any case, an 11h growth step probably wouldn't be 
practical anyways.

I was impressed that there was no repression at the 0h timepoint.  Cas9 is 
under the control of estradiol, which I only added at the 0h timepoint, but I 
would've expected there to be some leaky expression overnight.

.. figure:: 20171024_on_off_controls.svg
   :align: center

   Dashed lines: off; Solid lines: on.  Traces represent the indicated growth 
   times.

