****************************************
sgRNA Sensor --- General-Purpose Scripts
****************************************

These scripts automate various tasks associated with the sgRNA sensor project, 
most notably generating and displaying the sequences of rational designs.

Installation
============
Download the scripts using ``git``::

   $ git clone git@github.com:kalekundert/sgrna_sensor_scripts.git

The repository contains includes the ``sgrna_sensor`` library that is used by 
many of the scripts (and some of the protocols__).  Follow the instructions `on 
this page`__ to install it.  Every other library required by these scripts will 
be automatically installed along with the ``sgrna_sensor`` library.

__ https://github.com/kalekundert/sgrna_sensor_protocols
__ sgrna_sensor/

Usage
=====
Use the ``./show_seqs.py`` script to look at sequences for specific designs.  
for example, to see the sequence of the wildtype sgRNA::

   $ ./show_seqs.py wt
   GGGGCCACTAGGGACAGGATGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU

By default, different domains are displayed in different colors:

- Green: Upper and lower stem
- Red: Nexus
- Blue: Hairpins
- Orange: Aptamer

There are many different options to control how the sequences are printed, and 
you can see all of them using the ``--help`` flag.  But some of the most useful 
are ``-d`` to print DNA sequences, ``-S`` to exclude spacer (i.e.  targeting) 
sequences, ``-b`` to display sequences in a tab-separated format that can be 
easily copied into the IDT order form, ``-f`` to display sequences in the FASTA 
format, and ``-r`` to predict 2° structures of the RNA constructs (this will 
only work if you installed the python bindings to ViennaRNA)::

   $ ./show_seqs.py wt -d
   GGGGCCACTAGGGACAGGATGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT

   $ ./show_seqs.py wt -S
   GUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU

   $ ./show_seqs.py wt -b
   wt      	TATAGTAATAATACGACTCACTATAGGGGGCCACTAGGGACAGGATGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT

   $ ./show_seqs.py wt -f
   > wt
   GGGGCCACTAGGGACAGGATGTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT

   $ ./show_seqs.py wt -r
   GGGGCCACUAGGGACAGGAUGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU
   ...........((((((..((((((((.((((....))))...))))))))...)).)))).......((((....))))(((((((...)))))))..... (-25.50)
   ,({,..,,,{.((((((..((((((((.((((....))))...))))))))...)).)))).}......|||....||}}|((((((...})))))).,,,. [-28.01]
   ...........((((((..((((((((.((((....))))...))))))))...)).))))...................(((((((...)))))))..... {-23.80 d=11.61}
   .........(.((((((..((((((((.((((....))))...))))))))...)).)))).).................(((((((...)))))))..... {-23.60 MEA=81.84}
    frequency of mfe structure in ensemble 0.0171703; ensemble diversity 18.24

Use the ``./show_batch.sh`` script to show groups of sequences that I ordered 
and tested together.  The first argument to this script must be the number of a 
batch (or "all").  After that any option understood by ``show_seqs.py`` may be 
provided::

   $ ./show_batch.sh 1 -f
   > us(0,0)
   GGGGCCACTAGGGACAGGATGTTTTAGAATACCAGCCGAAAGGCCCTTGGCAGAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT
   > us(0,1)
   GGGGCCACTAGGGACAGGATGTTTTAGATATACCAGCCGAAAGGCCCTTGGCAGTAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT
   > us(0,2)
   GGGGCCACTAGGGACAGGATGTTTTAGATTATACCAGCCGAAAGGCCCTTGGCAGTTAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT
   > us(0,3)
   GGGGCCACTAGGGACAGGATGTTTTAGATTTATACCAGCCGAAAGGCCCTTGGCAGTTTAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT


