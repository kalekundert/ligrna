*************************
Titrate candidate sensors
*************************

We want figure 2 to include in vivo titrations for all of our successful 
designs.  Previously we'd collected single biological replicates for ``mhf 30`` 
and ``mhf 37``, but nothing for ``rxb 11,1``.  The purpose of this experiment 
is to collect three biological replicates for each sensor, of good enough 
quality to include in the paper.

Protocol
========

This protocol was repeated on thee different days, specifically:

- Mar 23, 2017
- Mar 29, 2017
- Mar 31, 2017

I picked a different colony each day, but all the colonies came from the same 
transformation.

.. command-output:: protocols/crispri_titration.py
    :cwd: /..

Results
=======
::

    $ ./titration_curve.py data/20170323_titrate_rxb_mhf.yml -N -m mode

.. figure:: 20170323_titrate_rxb_mhf.svg

As expected, the ``mhf`` sensors are activated by ligand and the ``rxb`` sensor 
is inhibited by it.  The titration is linear over almost 2 logs of theophylline 
concentration (20 uM to 1 mM).  

The replicates for ``rxb 11,1`` were very consistent.  In fact, they were more 
consistent than the controls, which is a little suspicious.  The ``mhf`` 
sensors were less consistent.  I want to see the ``fold_change.py`` traces for 
all the sensors, to reassure myself that nothing unexpected is going on, 
especially since I saw a lot of bimodal-looking traces (probably indicating 
Cas9 plasmid loss) as the data was being collected.  However, first I need to 
refactor ``fold_change.py`` to be able to read titration YAML files.

I could include the data from the first time I did this experiment, and from 
the experiment James did just prior to EBRC.  That would give me five 
replicates for the ``mhf`` sensors, four for ``rxb 11,1``, and still just three 
for the controls.  I didn't do this initially because I wanted to have the same 
number of replicates for everything, but now I'm thinking the more replicates 
the better.

I uses the ``gfp`` spacer for this experiment because it gives the best 
response to theophylline.  In retrospect, maybe it would've been better to use 
a spacer that was never part of the selection, specifically ``rfp2``.  

