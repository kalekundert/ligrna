***************************************
sgRNA Sensor --- Experimental Protocols
***************************************

This repository contains the experimental protocols I've used in the course of 
my work to develop small-molecule responsive sgRNA constructs.  It's really 
important to me that these protocol be reproducible, so please let me know if 
you encounter any errors or ambiguities.

Installation
============
All of the scripts in this repository require ``python3``.  Different systems 
have different ways of installing ``python3``, so I won't talk about it any 
more here, but usually it's not hard.

Some of the scripts additionally require third-party packages:

- ``dirty_water``: Format protocols and calculate reagent tables.
- ``docopt``: Parse command-line arguments.
- ``nonstdlib``: General-purpose utilities.
- ``pandas``: Manipulate tabular data.
- ``sgrna_sensor``: Get the sequences of rationally designed sgRNAs.

Except ``sgrna_sensor``, all of these dependencies can be installed from PyPI::

   $ pip3 install dirty_water docopt nonstdlib pandas

The ``sgrna_sensor`` dependency has to be installed from source from the 
``sgrna_sensor_scripts`` repository that accompanies this one on GitHub.  
Complete installation instructions can be found there__, but the process 
basically involves cloning the scripts repository and running ``pip`` on the 
downloaded source code::

   $ git clone git@github.com:kalekundert/sgrna_sensor_scripts scripts
   $ pip install ./scripts/sgrna_sensor

__ https://github.com/kalekundert/sgrna_sensor_scripts/tree/master/sgrna_sensor

Usage
=====
Some of the protocols are simple text (*.txt) files.  To view these, just open 
them in any text viewer.  For example::

   $ less make_cas9/buffer_list.txt

The rest of the protocols (i.e. most of them) are python scripts which can
automatically calculate how much of each reagent you'll need and things like 
that.  To view these protocols, just run them::

   $ ./cas9_cleavage_assay.py --help

If you want to print out paper copies of any of these protocols, try using the
``wet_copy`` package.  It automatically formats protocols so they can be pasted 
into a lab notebook (while leaving a margin for notes) and adds useful header 
information::

   $ pip install wet_copy
   $ wet_copy './cas9_cleavage_assay.py 2'

It's possible that you'd have to configure ``lpr`` to get ``wet_copy`` to work 
properly, but I think CUPS takes care of this on modern Linux and Mac systems.

