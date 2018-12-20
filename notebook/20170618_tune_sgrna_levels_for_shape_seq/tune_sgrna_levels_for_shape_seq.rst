*******************************
Tune sgRNA levels for SHAPE-Seq
*******************************

The first round of SHAPE-Seq experiments showed no change in reactivity due to 
either Cas9 or theophylline.  Kyle has seen Cas9 cause a change in reactivity 
for the controls in his own work, so we think this result simply indicates that 
there is an excess of sgRNA in the system.

There are two obvious ways to address this.  The first is to use a weaker 
promoter.  In his work, Kyle used the same strain and plasmid as I am, but he 
used the J23150 promoter, which is a relatively weak Anderson promoter.  I'm 
currently using the J23119 promoter, which is the strongest Anderson promoter.  
Kyle still got good repression with the weaker promoter, and he was able to 
observe a difference in reactivity upon the addition of Cas9, so it's very 
likely that this would help.

The second way to address this problem is to move the experiment in vitro.  
This would give us complete control over the concentrations of all species in 
the reaction.  The downside is that not all the designs work especially well in 
*in vitro*, so that might limit the change in reactivity we observe.  This 
approach would also require a little bit of cloning: I would need constructs 
with the T7 promoter and the terminator Kyle gave me.

Cloning the J23150 constructs
=============================
The `J23150 sequence <http://parts.igem.org/Part:BBa_J23150>`_ is::

   >BBa_J23150 Part-only sequence (35 bp)
   tttacggctagctcagtcctaggtattatgctagc

Here are the primers:

.. literalinclude:: ./20170618_j23150_primers.txt

These primers are for use with the `gfp` spacer.  The forward primer only 
extends 5 bp into the sgRNA, so I don't need different primers for `mhf 37`.  

I wonder if it would be worth doing a screen with J23150.  The idea is that 
such a screen would identify sensors that work at more even ratio of 
Cas9:sgRNA, which might make them more transferable.

Cloning the T7 constructs
=========================
There are two ways to do this: put the T7 promoter (and an appropriate spacer) 
into the SHAPE plasmids I already have, or put the SHAPE terminator into one of 
the *in vitro* plasmids I already have.  Both backbones have EcoRI and HindIII 
in the appropriate places, so that's not a concern.  The T7 promoter and the 
spacer sequence are 46 bp combined, while the SHAPE terminators are 71 bp.  I 
can't really think of any other differences to go on, so I guess I'll opt for 
the shorter primers and clone the T7 promoter into the vectors that already 
have the right terminator.

The other decision is what spacer to use.  It doesn't really matter, we just 
need the reactivity pattern to change in the presence of theophylline and/or 
Cas9 enough to be observable by SHAPE-seq.  `d1` is a good choice for `rxb 
11,1` (best spacer, and largest fold change for any spacer with any design at 
71.7%) and `mhf 30` (second best spacer after `d4`), but not for `mhf 37`.  
`d3` and `d2` are the best for `mhf 37` (in that order).  These activities 
might also change if we lower the ratio of sgRNA to Cas9 in the reaction, which 
we very well may do.  The question is whether I should cherry-pick the best 
spacer for each design (what about the controls then?) or just use the same 
spacer for all of them.  My instinct is that doing them all the same (with 
`d1`) would be best, but perhaps we'll have to come back and pick a different 
spacer for `mhf 37`.

.. literalinclude:: ./20170618_t7_primers.txt

I also need the following primer for `mhf 37`::

    Primer name (ready to copy into Elim form):
    T7_D1_MHF_37_TM_57_FOR

    Primer sequence (ready to copy into Elim form):
    CACTATAGGGGAACTCAAGAGCGGAGGGGTTTcagagcatgctggaaac

