#!venv/bin/python2.7

"""\
- Download the supplementary code from Doench16_::

      $ curl -O http://www.nature.com/nbt/journal/v34/n2/extref/nbt.3437-S3.zip

- Unpack the files::

      $ unzip nbt.3437-S3.zip
      $ tar -xzf Code/Rule_Set_2_Score.tar.gz

- Create a virtual environment to run the code in.  This is necessary both 
  because the script is ``python2`` and because it requires a very specific 
  version of ``scikit-learn`` in order to unpack its pickles::

      $ virtualenv -p python2.7 venv
      $ source venv/bin/activate

- Install the dependencies.  For some reason this has to be done in two steps::

      $ pip install numpy scipy pandas matplotlib biopython
      $ pip install scikit-learn==0.16.1

- The ``rs_score_calculator.py`` script has to be run from the directory it 
  lives in::

      $ cd Rule_Set_2_scoring_v1/analysis
      $ python rs2_score_calculator.py --seq AAAAAAAAAAAAAAAAAAAAAAAAAGGAAA
      Rule set 2 score: 0.2183

The Doench16_ rules take 30 bp sequences which contain some context before and 
after the spacer itself, specifically ``NNNN[spacer]NGGNNN``.  I need my 
spacers to start with ``GGG``, so I generated spacers from this pattern: 
``NNNNGGG[17×N]NGGNNN``.  I set the random seed to 0 to make the results 
reproducible.

.. [Doench16] Doench et al. *Optimized sgRNA design to maximize activity and 
   minimize off-target effects of CRISPR-Cas9.* Nat Biotechnol (2016) 
   34:2:184-191.
"""

import os, pickle
import random; random.seed(0)
import sys; sys.path.append('Rule_Set_2_scoring_v1/analysis')
from model_comparison import predict as rule_set_2
from pprint import pprint

num_spacers = 48
filter_factor = 2

model_file = 'Rule_Set_2_scoring_v1/saved_models/V3_model_nopos.pickle'
with open(model_file, 'rb') as file:
    model = pickle.load(file)    

def generate_spacer(): #
    # Start the spacer with 'GGG' so T7 can efficiently transcribe it.
    n = lambda n: ''.join(random.choice('ATGC') for _ in range(n))
    return n(4) + 'GGG' + n(18) + 'GG' + n(3)

def score_spacer(spacer): #
    return rule_set_2(spacer, -1, -1, model=model)

if __name__ == '__main__':
    spacers = []
    num_spacers = 48

    while len(spacers) < num_spacers:
        name = 'd{}'.format(len(spacers) + 1)
        spacer = generate_spacer()
        score = score_spacer(spacer)

        if score > 0.5:
            spacers.append((name, spacer, score))

    tsv_path = os.path.join(
            os.path.dirname(__file__), '..', 'doench_spacers.tsv')

    with open(tsv_path, 'w') as file:
        for row in spacers:
            file.write('\t'.join(str(x) for x in row) + '\n')


