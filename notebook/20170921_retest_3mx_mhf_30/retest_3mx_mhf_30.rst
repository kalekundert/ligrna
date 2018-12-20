*****************
Retest 3mx mhf 30
*****************

For our figure on multiplexing with theo and 3mx, we made a panel showing how 
mhf/30 and rxb/11 respond to ligand with both aptamers:

.. figure:: theo_and_3mx.svg
   :align: center

The glaring problem with this data is that the 3mx/mhf/30 construct just has 
more RFP expression than any of the other constructs, which shouldn't be the 
case.  In other words, theo/mhf/30 and 3mx/mhf/30 only differ by a single 
nucleotide, but the latter has almost 2x more RFP expression in the apo 
condition.

At first I thought this was an issue with data normalization, but it persists 
if you either don't normalize of size or normalize by the SSC channel instead 
of the GFP one.  It also persists if you normalize relative to the negative 
control.  The effect is also clearly present in the cell population traces, so 
it's really in the data.

That said, I don't really believe it because the data is low quality.  It's 
from James' ligand screen; he collected 9 replicates, but 6 of them have really 
messy peaks and the other 3 don't agree with each other very well.  The purpose 
of this experiment is to remake the data for this figure, hopefully so that 
it'll make more sense.

Methods
=======
Use the following ligands:

- 70 mM NaOH (apo)
- 30 mM caffeine + 70 mM NaOH (caff)
- 30 mM theophylline + 70 mM NaOH (theo)
- 30 mM 3-methylxanthine + 70 mM NaOH (3mx)

Prepare the media as follows:

- 2 mL 2x EZCCA
- 133.3 μL apo/caff/theo/3mx
- 1.86 mL milliQ water

.. literalinclude:: 20170921_crispri_assay.txt

Results
=======
I still see the same result as before, where the 3mx/mhf/30 construct has a 
dynamic range that's just shifted relative to theo/mhf/30.

.. figure:: 20170920_rfp2_mhf_30_theo_3mx.svg

As before, this shift is present in the raw cell distributions, so it's not 
just an artifact of how the data is normalized.  A small thing worth noting is 
that the fold change of the 3mx aptamer with 3mx isn't very good.  I'm 
suspicious that fresh 3mx might work better.

.. figure:: 20170920_rfp2_mhf_30_theo_3mx_fold_change.svg

In retrospect, it's not entirely unreasonable that the mutation that 
distinguished the two aptamers could affect the dynamic range because we do 
suspect that mhf/30 works by forming base-pairing interactions between the 
aptamer and other parts of the sgRNA.  I did a secondary structure prediction 
to look at this more closely:

.. figure:: theo_mhf_30_3mx_mhf_30.svg

The difference is a C→A mutation about ⅔ of the way into the aptamer.  There is 
a small difference around that position in the ensemble prediction::

          *
    theo: CUUGGCA
          ...||((

          *
    3mx:  AUUGGCA
          ,,||||,

This indicates to me that the 3mx aptamer spends more time base-paired with the 
5' side of the sgRNA, probably with the nexus, although I haven't looked 
closely enough to see what the actual base pairs might be.  Since these base 
pairs are what we believe turns the sgRNA "off", this could justify why mhf/30 
with the 3mx aptamer is more "off" than mhf/30 with the theo aptamer.
