*************************
Compare J23119 and J23150
*************************

Although I've used the very strong J23119 promoter for all my experiments so 
far, Kyle is using the weaker J23150 promoter for the SHAPE-Seq experiments.  
(He tried the J23119 promoter, but there was too much RNA and all we could see 
was the ligand-unbound, Cas9-unbound state.)  He collected initial data showing 
that the designs perform equally well with both promoters, and the goal of this 
experiment is to confirm that result.  It'd be nice if we could show that our 
designs weren't sensitive to the level of sgRNA expression.

Methods
=======
Oct 9, 2017: When transforming into mg1655, I'm worried that I might've mixed 
up the J23119 and J23150 transformations.  (The designs --- i.e. on, off, 
rxb/11/1, mhf/30, mhf/37 --- were definitely *not* mixed up.)  To be sure, I'm 
gonna miniprep and sequence the transformed cells.

Oct 10, 2017: I forgot to take the plastic cover off the overnights, but they 
still seemed to be pretty much saturated, so I continued with the experiment as 
usual.  I grew the cells for about 8h10.

Oct 11, 2017: I grew the cells for about 8h40, because I was in a meeting with 
Tanja when 8h happened.

Oct 12, 2017: I didn't have quite enough EZCCA media for all the reactions, so 
I used 985 μL media per culture and inoculated with 3.94 μL of overnight.  I 
grew the cells for about 8h10.

.. literalinclude:: 20171010_crispri_assay.txt

Results
=======
From what I remember of Kyle's data, I was expecting there to be no difference 
between J23119 and J23150.  However, the difference I see here makes more 
sense: the weaker promoter is shifted towards more full activation.  Presumably 
we could also get more full repression by using a weaker promoter for the 
reporter genes, or by repeating our screens with a weak promoter.

It's also noteworthy that the fold changes for rxb/11/1 and mhf/30 go down, but 
that for mhf/37 goes up.  The dynamic range (i.e. the difference between the on 
and off controls) doesn't change.

.. figure:: 20171010_compare_promoters.svg
