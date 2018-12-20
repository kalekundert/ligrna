********************
Improve yeast strain
********************

I recently started running selection experiments in yeast, but in the process 
I've found that my yeast strain isn't very healthy.  I discussed this with the 
El-Samad lab, and our initial thought is that this is due to the insertion at 
the His locus interfering with a downstream gene.  My goal here is to better 
characterize this problem, and repair it if possible.

Background
==========

Strains and genotypes
---------------------
I wasn't familiar with yeast genotype nomenclature, so I found [1]_ and [2]_ 
helpful for learning how to interpret them.  This excerpt from [1]_ was 
particularly helpful:

   Whenever possible, each gene, allele, or locus is designated by three 
   italicized letters, e.g., *ARG*, which is usually a describer, followed by a 
   number, e.g., *ARG2*.  Unlike most other systems of genetic nomenclature, 
   dominant alleles are denoted by using uppercase italics for all letters of 
   the gene symbol, e.g., *ARG2*, whereas lowercase letters denote the 
   recessive allele, e.g., the auxotrophic marker *arg2*.  Wild-type genes are 
   designated with a superscript "plus" (*sup6⁺* or *ARG2⁺*).  Alleles are 
   designated by a number separated from the locus number by a hyphen, e.g., 
   *arg2-9*.  The symbol *Δ* can denote complete or partial deletions, e.g., 
   *arg2-Δ1*.  [KBK: It took me a while to figure out that the number after the 
   Δ is just a way to refer to a specific deletion, e.g. was the whole gene 
   deleted, was just a particular domain deleted, etc.  You have to look online 
   to know which deletion each number refers to.] (Do not use the symbols 
   *Δarg2* or *arg2Δ* for deletions.) Insertion of genes follow the bacterial 
   nomenclature by using the symbol *::*.  For example, *arg2::LEU2* denotes 
   the insertion of the *LEU2* gene at the *ARG2* locus in which *LEU2* is 
   dominant (and functional) and *arg2* is recessive (and defective).

   Phenotypes are denoted by cognate symbols in roman type and by the 
   superscripts ⁺ and ⁻.  For example, the independence and requirement for 
   arginine can be denoted by Arg⁺ and Arg⁻, respectively.  Proteins encoded by 
   *ARG2*, for example, can be denoted Arg2p, or simply Arg2 protein.  However, 
   gene symbols are generally used as adjectives for other nouns, for example, 
   *ARG2* mRNA, *ARG2* strains.  Resistance and sensitivity phenotypes are 
   designated by superscript R and S, respectively.  For example, resistance 
   and sensitivity to canavanine sulfate are designated Can\ :sup:`R` and Can\ 
   :sup:`S`\ , respectively.

   Although most alleles can be unambiguously assigned as dominant or recessive 
   by examining the phenotype of the heterozygous diploid crosses, dominant and 
   recessive traits are defined only with pairs, and a single allele can be 
   both dominant and recessive.  For example, because the alleles *CYC1⁺*, 
   *cyc1-717*, and *cycl-Δ1* produce, respectively, 100%, 5%, and 0% of the 
   gene product, the *cyc1-717* allele can be considered recessive in the 
   *cyc1-717*/*CYC1⁺* cross and dominant in the *CYC1-717*/*cyc1-Δ1* cross.  
   Thus, it is less confusing to denote all mutant alleles by lowercase 
   letters, especially when considering a series of mutations having a range of 
   activities.

The strain I'm using is yBMH127, which has the following genotype:

   pRNR2-GEM-tSSA1-pGal1-dCas9MXI1-tADH1(Ura)
   pTDH3-UBI-Y-Venus(His)

yBMH127 is derived from yAHN321, which has just the dCas9 cassette:

   pRNR2-GEM-tSSA1-pGal1-dCas9MXI1-tADH1(Ura)

yANH321 is derived from BY4741, which is a commonly used haploid strain that 
has several metabolic marker genes completely deleted:

   MATa his3Δ1 leu2Δ0 met15Δ0 ura3Δ0

   BY4741 is part of a set of deletion strains derived from S288C in which 
   commonly used selectable marker genes were deleted by design in order to 
   minimize or eliminate homology to the corresponding marker genes in commonly 
   used vectors without significantly affecting adjacent gene expression. The 
   yeast strains were all directly descended from FY2, which is itself a direct 
   descendant of S288C. Variation between BY4741 and S288C is miniscule. BY4741 
   was used as a parent strain for the international systematic Saccharomyces 
   cerevisiae gene disruption project.

   http://www.yeastgenome.org/strain/BY4741/overview

HIS3 may interfere with DED1
----------------------------
HIS3 is immediately upstream of the essential gene DED1.  This is relevant for 
two reasons.  First, insertions at the HIS3 locus have the potential to affect 
the expression level of DED1.  We believe that this is the cause of the growth 
defect I'm observing.  Second, the HIS3 deletion in BY4741 (his3Δ1) is only 
partial because the full deletion does affect DED1.  Specifically, his3Δ1 is a 
187 bp deletion in a 663 bp ORF.  This partial deletion brings back the problem 
of yeast recombining just the repaired marker and not whatever else you want to 
transform.

Why hasn't this come up before?
-------------------------------
The El-Samad lab uses yeast for everything, so it was fair to ask why this 
growth defect hadn't been a problem before.  The answer is a little bit of a 
history lesson.

Initially, the El-Samad lab used a strain that just had mutations in its 
selectable genes, rather than those genes being completely deleted.  Ben told 
me the name of the strain, but I can't remember what it was, maybe W303?  The 
advantage of this approach is that it left the genetic context of the 
selectable markers unchanged, which is important for studying yeast biology.  
The disadvantage is that it made it easy for the yeast to get just the marker 
by homologous recombination and not the gene you wanted to clone in.

Apparently the HIS3 marker was especially prone to not working, so the lab just 
got used to not using it.  The problem of unwanted recombination was eventually 
solved by using markers from other species (i.e. with little homology to the 
*S. cerevisiae* markers), but people stayed in the habit of avoiding HIS.

The El-Samad lab only recently started using BY4741, which they got from the 
Duber lab.  I'm not sure why the Duber lab hasn't encountered and fixed this 
problem already, though.

Solution: a new HIS3 cassette
-----------------------------
To solve the problems with the HIS marker, the El-Samad lab is creating a new 
HIS3 cassette that has homology with a totally different part of the genome.  
(Andrew told me where, but I can't remember now.)  Ben used this cassette to 
create the strains yBMH138 and yBMH139.  Both strains are in the context of 
dCas9-MxiI and have the fluorescent reporter inserted in the new location.  The 
former strain just has Venus while the latter one has Ub-Y-Venus.


Methods
=======

Growth rates --- Aug 5, 2017
----------------------------
1. Start 3 mL overnight cultures in YPD for both yAHN321 and yBMH127

2. Inoculate two 100 mL YPD cultures with all 3 mL of each overnight.

3. Incubate at 30°C with shaking at 225 rpm.  Measure the OD600 of both 
   cultures at semi-regular intervals (aiming for about 1 measurement/hour).

Growth rates --- Aug 24, 2017
-----------------------------
Measure the growth rate of just yBMH139 in the course of doing a competent cell 
prep.

1. Start a 5 mL BMH139 overnight culture in YPD from a colony picked from a 
   SD-His plate.  The plate hadn't really been in the incubator long enough at 
   the time, so the colony I picked was pretty small.

2. Inoculate a 132 mL YPD culture with all 5 mL of the overnight.  The 
   overnight was pretty thin, so the culture started off very dilute.

3. Incubate at 30°C with shaking at 225 rpm.  Measure the OD600 of the culture 
   at semi-regular intervals.


Results
=======

Growth rates
------------
Before spending a lot of time constructing a new strain, I wanted to be sure 
that yBMH127 actually has a growth defect (previously I'd only noted in 
anecdotally).  I also wanted to be sure that yAHN321 didn't have a growth 
defect, which would support the idea that the HIS3 locus is the problem.  I 
addressed these questions by growing yANH321 alongside yBMH127 that I was 
growing for a competent cell prep, and measuring OD every hour or so.

====  ===============  ===============
Time  OD600 (yAHN321)  OD600 (yBMH127)
====  ===============  ===============
0h00  0.3193           0.2755
3h15  0.3759 × 3       0.1869 × 3
4h05  0.5451 × 3       0.2395 × 3
5h00  0.6521 × 4       0.2387 × 4
6h15  0.9923 × 4       0.3391 × 4
6h50  1.0091 × 5       0.3295 × 5
====  ===============  ===============

I decided to discard the last two data points for yAHN321 because I think they 
got outside the linear range of the spectrophotometer.  With those points 
included, the t½ for yAHN321 goes up to 104.5 min.

There's clearly a growth defect caused by the YFP gene.  The parent strain 
grows at the rate you'd expect for healthy yeast (t½=90m).  The YFP strain, on 
the other hand, takes almost 2h30 to double.

.. figure:: ahn321_bmh127.svg

Growth rates
------------
The growth defect appears to be repaired in yBMH139.  I didn't test yBMH138 
because I prefer using the fluorescent protein with the degradation tag.

====  ===============
Time  OD600 (yBMH139)
====  ===============
0h00  0.0247
1h55  0.0582
3h49  0.1397
5h54  0.3712
7h04  0.3309 × 2
8h08  0.3644 × 3
====  ===============

The doubling time is exactly the same as the parent strain, and exactly what 
you'd expect for wildtype yeast (t½=90m).

.. figure:: bmh139.svg

The strain is also brightly fluorescent:

.. figure:: 20170824_bmh139_yfp_check.svg

References
==========
.. [1] Sherman. Getting started with yeast. Methods Enzymol (2002) 350:3-41

.. [2] http://www.yeastgenome.org/sgdpub/Saccharomyces_cerevisiae.pdf
