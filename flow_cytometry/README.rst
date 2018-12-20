***************************************
sgRNA Sensor --- Flow Cytometry Scripts
***************************************

The scripts in this repository help manage and visualize the results from flow 
cytometry experiments.  This includes both cell-counting (on the BD LSR II) and 
cell-sorting (on the BD FACSAria II).

Installation
============
Download the scripts using ``git``::

   $ git clone git@github.com:kalekundert/sgrna_sensor_flow_cytometry.git

You will also have to install ``fcmcmp``, a library for organizing and parsing 
flow cytometry data::

   $ pip install fcmcmp

Usage
=====
The most useful script is ``fold_change.py``, which shows 1D flow cytometry 
traces and calculates fold changes between the "apo" and "holo" conditions::

   $ ./fold_change.py path/to/input.yml

The ``input.yml`` file should describe how various wells will be compared to 
each other, and should be in the format described here__.

__ https://pypi.python.org/pypi/fcmcmp/0.1.0

