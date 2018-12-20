*****************************
Add antibiotic to yeast media
*****************************

When I was last doing screens, I had a couple problems with bacterial or fungal 
contamination.  First, ~30% of my library plates get contaminated, either by 
mold or by bright red colonies.  Second, one of my liquid-media libraries got 
taken over by (presumably) bacteria.  (The bacteria had a very distinct smell; 
I don't think they came from our lab, but maybe the came from the sorter).  To 
prevent contamination like this in the future, I'm looking into antibiotics I 
can add to my media.

Pen/Strep
=========
I began by asking the Dueber lab how they deal with contamination.  The answer 
I got:

   For antibiotics, I use pen/strep. You can buy it at 100x and just add it to 
   the agar before you pour it. Top plating should also work if you already 
   have the plates. I've never tried it. I still sometimes get fungal 
   contamination on library sized plates so I started just using 36 regular 
   plates instead haha. 

Pen/strep isn't active against mold, and I'm getting contamination even though 
I'm already using regular plates, so I'll still need to find a way to deal with 
that.  But it's probably not a bad idea to have a defense against bacterial 
contamination as well.

Both penicillin and streptomycin are bactericidal.  Penicillin works by 
inhibiting cell wall synthesis.  This causes the cells to shed their walls when 
they divide, rendering them very fragile and sensitive to osmotic pressure.  
Streptomycin works by interfering with ribosomal proofreading, which leads to 
the synthesis of aberrant proteins.  The cells ultimately die because the 
membrane becomes more permeable as aberrant proteins insert into it, and the 
cells react by inducing a stress response that ultimately produces hydroxyl 
free radicals.

While I was reading about this, I got onto an interesting tangent because I 
thought streptomycin was just bacteriostatic.  Antibiotics that inhibit 
translation *are* just bacteriostatic, but antibiotics that interfere with 
proofreading are bactericidal.  This is an important distinction, because 
penicillin is inhibited by bacteriostats [Ocampo2014]_.  The reasoning is 
simple: cell wall inhibitors are only lethal if cells are dividing, and 
bacteriostats prevent them from dividing.

Other antibiotics
=================
This page from [Sigma]_ shows a wide variety of antibiotics that target 
bacteria but not yeast, including carbenicillin, chloramphenicol, and 
kanamycin.  These would be convenient because I'm already used to using them, 
so they might be worth a try.

Sterile technique
=================
Adding antibiotics won't help with my library plates, because there aren't any 
antibiotics that can distinguish between yeast and mold (both are fungi).  This 
led me to think about improving my sterile technique.

In particular, I'm suspicious that it's a bad idea to leave my plates with 
their lids off while they're cooling, even if I have them near a flame.  The 
reason I do this is to prevent condensation from collecting on the lids, but I 
thought I might find look online to see if I could find a better approach.  
[Addgene]_ suggests covering the plates immediately, but leaving them on the 
bench overnight to allow the condensation to reabsorb into the agar.  They also 
suggest pouring the agar rather than pipetting it each time.  I can believe 
that that would be easier and more sterile, but I think I'm going to stick with 
pipetting because it's probably best if all my plates have the same amount of 
media, so I don't get more growth on some plates than others.

I also found a good general introduction to sterile technique from [KSU]_.  
According to it:

   The most common sources of contamination during an experiment are dust, from 
   the bench top, from the air and from people. This dictates several obvious 
   principles:

   1) Keep things covered as much as possible.
   2) Don't touch anything that will come in contact with the culture and if you do touch it sterilize it again before using it.
   3) Wipe down the surface around the experiment with alcohol and minimize air turbulence.
   4) Avoid talking, singing, whistling, coughing, or sneezing in the direction of things that should be sterile. Long hair, if not tied back, may be a source of contamination.
   5) Maintain a suitable area for preparing, storing, and using sterile media.  
      Unfortunately, house plants, animals, and other materials such as 
      Drosophila media, commonly found in biology class rooms, are abundant 
      sources of mold and must be kept far away from the area used for sterile 
      procedures. 

I think these are all good things to keep in mind.  I haven't been wiping my 
bench down with ethanol, so I'll start doing that, too.

References
==========
.. [Ocampo2014] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4135978/

.. [Sigma] http://www.sigmaaldrich.com/life-science/core-bioreagents/learning-center/antibiotic-selection.html

.. [Addgene] https://www.addgene.org/protocols/pouring-lb-agar-plates/

.. [KSU] https://www.phys.ksu.edu/gene/g1.html


