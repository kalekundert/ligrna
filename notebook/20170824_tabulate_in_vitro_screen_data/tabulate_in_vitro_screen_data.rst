*****************************
Tabulate in vitro screen data
*****************************

I want to create a table containing all the data from my in vitro screen, which 
I may want to include in the supplement.  I'm not sure this data will be easy 
to collect.  I'll have to go through my old lab notebooks to see which images 
correspond to which designs.

Methods
=======
I went back through my notebook, found all the gels from the screens, and redid 
all of the densiometry analysis.  I did the analysis differently for the gels 
with 500 bp target DNA (i.e. my earlier experiments).  For those, I wasn't 
comfortable subtracting the background because the signal was barely above the 
background as it was and I didn't trust the smoothing algorithm to not just 
totally obliterate the data.  So instead I just drew the baselines myself.  In 
many cases they should've been slightly curved, but I just approximated them as 
best I could with straight lines.  For the 4kb gels, I subtracted the baseline 
with a 50px radius, and drew a straight baseline 1-3 px above 0 to separate the 
peaks as necessary.

I saved the results of each densiometry analysis in a separate XLSX file, then 
wrote a python library --- `sgrna_sensor.densiometry` --- to parse these files.  
Then I wrote the `make_tables.py` script to tabulate the data from the in vitro 
screen.

Results
=======
- :download:`summary_table.pdf`
- :download:`full_table.pdf`
