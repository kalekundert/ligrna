- I chose to use the "full-length" osmY promoter for the fluorescent proteins.  
  I had to choose a promoter other than J23119, because the PCR primers I will 
  need to install the N20 targeting sequence overlap with the J23119 promoter 
  controlling the sgRNA, and that PCR reaction will not work well if that same 
  promoter sequence is present in several places on the plasmid.  
  
  I decided against solving this problem by putting the sgRNA under the control 
  of another promoter, because J23119 (apparently) has a very consistent start 
  site.  This consistency is important because the spacer sequence starts right 
  away, and variations in the length of the spacer sequence can significantly 
  affect how well the whole system works [1].  Since I don't think I can really 
  be sure which promoters are more or less consistent, I decided to keep the 
  sgRNA under the control of the J23119 promoter.
  
  The majority of the constitutive promoters that have been characterized 
  (including J23119) are σ70 promoters.  Unfortunately, all of these promoters 
  seemed homologous enough that they could still cause problems for PCR.  
  Instead, I decided to use the osmY promoter, which is a σS promoter.  Genes 
  under the control of this promoter are expressed when the bacteria reach 
  stationary phase, which is perfect for this assay.  I don't want the cells to 
  grow differently based on how much fluorescent protein they're expressing, so 
  deferring that expression until the cells have reached stationary phase and 
  stopped growing is perfect.

  There are two osmY promoters in the IGEM parts catalog, and full-length 
  version and a minimal version.  The difference between the two is that the 
  full-length promoter includes an extra 150 bp 5' of the promoter.  I decided 
  to use the full-length one because the minimal one was annotated as not 
  working, and I was able to find data showing the full-length one being used 
  to defer the expression of GFP until OD 0.6 [3].  
  
  However, I was conflicted about this because the original description of the 
  osmY promoter suggests that neither the full nor the minimal promoter is 
  ideal [4].  First, the authors show that the region 5' of the -36 position 
  has no affect on transcription.  Since the only difference between the 
  full-length and minimal promoters is in that region, they should both work 
  fine.  Second, the authors show that the region 3' of the +1 site but before 
  the start codon (i.e. the UTR) does affect transcription.  Since both the 
  full-length and minimal promoters omit this region, neither should work that 
  well.  Ultimately, I decided to use the full-length promoter because it's 
  been used with GFP and seems to work how I want.

- I decided to remove the rrnB T1 terminator that used to come after the sgRNA.  
  In the original pBLO2 plasmid, there were actually a few hundred base pairs 
  encoding two affinity tags (Myc and 6xHis) between the sgRNA and this 
  terminator, so if the terminator was being used, there was a lot of junk 
  hanging off the sgRNA.  I think this terminator was part of a MCS originally 
  intended for proteins but that was replaced by the sgRNA.  The sgRNA also has 
  its own terminator, so I don't really think this terminator was being used.

  I still considered keeping the rrnB T1 terminator just to make sure the sgRNA 
  is properly terminated, but I decided not to because I was worried it might 
  inadvertently terminate the GFP transcript on the opposite strand.  rrnB T1 
  is a unidirectional terminator, but it's not uncommon for even unidirectional 
  terminators to weakly terminate on the opposite strand, and I couldn't find 
  any specific data on how rrnB T1 affects the opposite strand.  I weighed the 
  possibility of run-on transcripts against the possibility of inadvertent 
  termination, and I decided that the latter was more of a concern.
  
- I decided to assemble the plasmid in a 5-part Gibson assembly, where the GFP 
  and RFP are split into separate parts and connected by a third part 
  containing the osmY promoter.  The alternative would've been to do a 3-part 
  assembly and to fix the RFP promoter after the fact using inverse PCR.  
  However, the 5-part approach gives me the ability to use the full-length osmY 
  promoter sequence, which is 200 bp long and too long to assemble by inverse 
  PCR.  The 5-part approach should also be faster and easier.

- I preferred to put the homology arms for the Gibson assembly in the gBlocks 
  rather than the PCR primers.  This might make it easier to swap out the 
  gBlocks later (e.g. to fiddle with the promoters) without having to redo the 
  PCR steps.

- I included an extra ~50 base pairs 3' of the RFP gene, so that the reverse 
  primer in the PCR reaction to extract RFP would only bind downstream of RFP 
  and not GFP.  This wouldn't really have been a problem anyway, because only 
  the primer that bound downstream of RFP could've amplified, but maybe this 
  will help make the PCR more efficient.

[1] Larson, Gilbert, Wang, Lim, Qi. CRISPR interference (CRISPRi) for 
sequence-specific control of gene expression. Nat Protoc. 2013 Nov; 8(11): 
2180-2196. 

[2] http://parts.igem.org/Promoters/Catalog/Anderson

[3] Voigt. Synthetic Biology: Methods for part/device characterization and 
chassis...  Chapter 12: BioBuilding: Using Banana-scented bacteria to teach 
synthetic biology.

[4] Yim, Brems, Villarejo. Molecular characterization of the promoter of osmY, 
an rpoS-dependent gene. J. Bacteriology (Jan 1994) 176:1:100-107.
