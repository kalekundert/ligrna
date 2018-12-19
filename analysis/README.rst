*********************************
sgRNA Sensor --- Design Sequences
*********************************

This library contains classes and functions that can be used to represent 
sgRNA/aptamer fusions.  The primary components of this repository are a set of 
classes that represent modular DNA or RNA sequences, a set of functions that 
return sgRNA designs according to various parameters, and a command line tool 
that can print sequences for those designs.

Installation
============
The first step is to download the scripts repository that contains this code 
from GitHub::

   $ git clone git@github.com:kalekundert/sgrna_sensor_designs.git

The second step is to install the library somewhere python can find it.  If you 
are using the system python, this command will require an administrator's 
password::

   $ pip install --editable ./sgrna_sensor_designs

The ``--editable`` flag will cause any changes you make to the repository to be 
immediately reflected in the installed library and command line tools.

The design library can predict RNA secondary structure if the python wrappers 
to the ViennaRNA package are installed.  I assumed that I had to compile 
ViennaRNA from source to get the python bindings, but in retrospect that might 
not have been necessary.  So try installing the binaries, and if that doesn't 
work use something like these commands to install ViennaRNA from source::

   # Download the ViennaRNA source:
   $ curl 'http://www.tbi.univie.ac.at/RNA/download/package=viennarna-src-tbi&flavor=sourcecode&dist=2_2_x&arch=src&version=2.2.5' -o ViennaRNA-2.2.5.tgz

   # Unpack the source archive:
   $ tar -xzf ViennaRNA-2.2.5.tgz
   $ cd ViennaRNA-2.2.5

   # Install dependencies (for Fedora 23, adjust as necessary for your OS):
   $ sudo dnf install                    \
         gsl-devel                       \
         swig                            \

   # Compile and install ViennaRNA:
   $ export CFLAGS="-w"
   $ export CPPFLAGS="-w"
   $ ./configure                         \
       --prefix /home/kale/.local        \
       --enable-gen-hard-constraints     \
       --with-python3                    \
       --without-perl                    \
       --without-kinfold                 \
       --without-forester                \
       --without-doc-pdf                 \
       --without-doc-html                \
   $ make && make install

Usage
=====
Use the ``sgrna_sensor`` script to look at sequences for specific designs.  For 
example, to see the sequence of the positive control sgRNA::

   $ sgrna_sensor on
   GUUUCAGAGCUAUGCUGGAAACAGCAUAGCAAGUUGAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU

By default, different domains are displayed in different colors:

- Green: Upper and lower stems
- Yellow: Bulge
- Red: Nexus
- Purple: Ruler
- Blue: Hairpins
- Orange: Aptamer

You can specify which spacer sequence to use as part of the design name::

   $ sgrna_sensor aavs/on
   GGGGCCACUAGGGACAGGAUGUUUCAGAGCUAUGCUGGAAACAGCAUAGCAAGUUGAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU

There are many different options to control how the sequences are printed, and 
you can see all of them using the ``--help`` flag.  Some of the most useful are 
``-d`` to print DNA sequences, ``-b`` to display sequences in a tab-separated 
format that can be easily copied into the IDT order form, ``-f`` to display 
sequences in the FASTA format, and ``-r`` to predict 2° structures of the RNA 
constructs (this will only work if you installed the python bindings to 
ViennaRNA)::

   $ sgrna_sensor on -d
   GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT

   $ sgrna_sensor aavs/on -b
   aavs_on 	TATAGTAATAATACGACTCACTATAGGGGGCCACTAGGGACAGGATGTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT

   $ sgrna_sensor on -f
   > on
   GTTTCAGAGCTATGCTGGAAACAGCATAGCAAGTTGAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGCTTTTTT

   $ sgrna_sensor on -r    
   GUUUCAGAGCUAUGCUGGAAACAGCAUAGCAAGUUGAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUUUU
   ........(((((((((....)))))))))(((((((.....((.....))....)))))))...((((.(((((((...))))))).)))) (-33.00)
   ........(((((((((....)))))))))(((((((..{,,{(.....}).}},))))))),,,{(({.(((((((...))))))).))), [-35.21]
   ........(((((((((....)))))))))(((((((.....((.....))....)))))))........(((((((...)))))))..... {-32.40 d=8.64}
   ........(((((((((....)))))))))(((((((...(.((.....))..).)))))))....(((.(((((((...))))))).))). {-29.60 MEA=77.14}
    frequency of mfe structure in ensemble 0.0279294; ensemble diversity 12.74
