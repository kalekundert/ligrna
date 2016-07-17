#!/usr/bin/env sh
set -euo pipefail

# Clean up old files
rm -rf results stdout
mkdir -p results/{no,example,random}_spacers stdout

# Submit the design jobs
qsub -t 1-50 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/no_spacers/mh_6" sgrna_mc
qsub -t 1-50 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/no_spacers/mh_7" sgrna_mc
qsub -t 1-50 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/example_spacers/mh_6" sgrna_mc
qsub -t 1-50 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/example_spacers/mh_7" sgrna_mc
qsub -t 1-50 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/random_spacers/mh_6" sgrna_mc
qsub -t 1-50 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/random_spacers/mh_7" sgrna_mc
