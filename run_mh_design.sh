#!/usr/bin/env sh
set -euo pipefail

# Clean up old files
mkdir -p stdout spacers no_spacers
rm -f stdout/* spacers/*.tsv no_spacers/*.tsv

# Submit the design jobs
qsub -t 1-30  -v "ADDAPT_ARGS=inputs/mh_6.yml -n16000 inputs/scorefxn.yml inputs/fast_anneal.yml,OUTPUT_PREFIX=results/no_spacers/mh_6" sgrna_mc
qsub -t 1-30  -v "ADDAPT_ARGS=inputs/mh_7.yml -n16000 inputs/scorefxn.yml inputs/fast_anneal.yml,OUTPUT_PREFIX=results/no_spacers/mh_7" sgrna_mc
qsub -t 1-100 -v "ADDAPT_ARGS=inputs/mh_6.yml -n16000 inputs/scorefxn.yml inputs/slow_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/example_spacers/mh_6" sgrna_mc
qsub -t 1-100 -v "ADDAPT_ARGS=inputs/mh_7.yml -n16000 inputs/scorefxn.yml inputs/slow_anneal.yml inputs/example_spacers.yml,OUTPUT_PREFIX=results/example_spacers/mh_7" sgrna_mc
qsub -t 1-100 -v "ADDAPT_ARGS=inputs/mh_6.yml -n16000 inputs/scorefxn.yml inputs/slow_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/random_spacers/mh_6" sgrna_mc
qsub -t 1-100 -v "ADDAPT_ARGS=inputs/mh_7.yml -n16000 inputs/scorefxn.yml inputs/slow_anneal.yml inputs/random_spacers.yml,OUTPUT_PREFIX=results/random_spacers/mh_7" sgrna_mc
