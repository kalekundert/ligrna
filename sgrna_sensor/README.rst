****************************************
sgRNA Sensor --- Rational Design Library
****************************************

This library contains classes and functions that can be used to rationally 
sgRNA/aptamer fusions.  The primary components of this library are a set of 
classes that represent modular DNA or RNA sequences and a set of functions that 
return sgRNA designs according to various parameters.

Installation
============
The first step is to download the scripts repository that contains this code 
from GitHub::

   $ git clone git@github.com:kalekundert/sgrna_sensor_scripts.git

The second step is to install the library somewhere python can find it.  If you 
are using the system python, this command will require an administrator's 
password::

   $ pip install ./sgrna_sensor_scripts/sgrna_sensor

The rational design library can predict RNA secondary structure if the python 
wrappers to the ViennaRNA package are installed.  I assumed that I had to 
compile ViennaRNA from source to get the python bindings, but in retrospect 
that might not have been necessary.  So maybe try installing the binaries, 
otherwise use something like these commands to install ViennaRNA from source::

   # Download the ViennaRNA source:
   $ curl 'http://www.tbi.univie.ac.at/RNA/download/package=viennarna-src-tbi&flavor=sourcecode&dist=2_2_x&arch=src&version=2.2.0' -o ViennaRNA-2.2.0.tgz

   # Unpack the source archive:
   $ tar -xzf ViennaRNA-2.2.0.tgz
   $ cd ViennaRNA-2.2.0

   # Install dependencies (for Fedora 23, adjust as necessary for your OS):
   $ sudo dnf install                    \
         autoconf                        \
         automake                        \
         gsl-devel                       \
         libtool                         \
         swig                            \

   # Compile and install ViennaRNA:
   $ export CFLAGS="-w"
   $ export CPPFLAGS="-w"
   $ ./configure                         \
         --prefix ~/.local               \
         --without-perl                  \
         --without-kinfold               \
         --without-forester              \
         --without-doc-pdf               \
         --without-doc-html              \
   $ make && make install

Usage
=====
The rational design library is mostly made available through the scripts in the 
top level of repository.  In particular, the ``show_seqs.py`` script is useful 
for visualizing individual designs in many different ways::

   $ ./show_seqs.py -h
