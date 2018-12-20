**********************
Analyze SHAPE-Seq Data
**********************

Kyle just sent me his SHAPE-Seq data and his analysis of it.  I'm working 
through it now, and making notes of any thoughts and questions I have.

mhf/30

- How did you do the thermodynamic folding predictions for mhf/30?  i.e. did 
  the two states appear in one ensemble, or did constraining the aptamer lead 
  to a change in predicted structure?

- What do the lines with square heads mean in the pictures?  Also, what program 
  did you use to make these structures?

- If ligand binding controls dCas9 binding, then we'd expect to see no 
  difference between dCas9 and neither.  However, dCas9 - neither looks pretty 
  much the same as theo - neither.

- dCas9/theo - theo should give just the effect of Cas9 binding.  That trace 
  looks pretty much the same as dCas9/theo - dCas9, which makes me think that 
  all the effects in the latter trace are simply driven by Cas9 binding.

- What does dCas9/theo - neither look like?

mhf/37

- You mention that the interaction between the bulged U forms and Cas9 involves 
  a carboxyl that all pyrimidines share.  Can you show this to me?  I don't see 
  any specific interaction in the crystal structure.

rxb/11/1

- rxb/11 works in vitro, with relatively stoichiometric levels of RNA, Cas9, 
  and DNA.  This isn't consistent with the idea that only trace quantities of 
  working RNA is present.  Unless maybe it's just a matter of time, and 
  eventually the U will flip out and Cas9 will bind.  I do run my in vitro 
  reactions for a long time.

- Thoughts about whether we can conclude which forms bind Cas9 from SHAPE data?  
  Looks to me like 'dCas9 - neither' shows the shifts due to Cas9 binding.
  'dCas9/theo - theo' shows the same shifts, so can we conclude that the sgRNA 
  binds Cas9 with or without ligand, and the ligand just controls whether Cas9 
  can function?

