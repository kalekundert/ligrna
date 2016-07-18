#!/usr/bin/env sh
set -euo pipefail

# Clean up old files
rm -rf results stdout
mkdir -p results/mh_design/{no,example,random}_spacers stdout

# Submit the design jobs
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/mh_design/random_spacers/mh_6" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/mh_design/random_spacers/mh_7" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/mh_design/example_spacers/mh_6" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/mh_design/example_spacers/mh_7" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_6.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/mh_design/no_spacers/mh_6" sgrna_mc
qsub -t 1-25 -v "ADDAPT_ARGS=inputs/mh_7.yml -n10000 inputs/scorefxn.yml inputs/auto_anneal.yml,OUTPUT_PREFIX=results/mh_design/no_spacers/mh_7" sgrna_mc
