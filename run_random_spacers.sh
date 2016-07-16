#!/usr/bin/env sh
set -euo pipefail

# Clean up old files
mkdir -p stdout random_spacers
rm -f stdout/* random_spacers/*.tsv

# Submit the design jobs
qsub -t 1-100 -v "ADDAPT_ARGS=mh_6.yml ../scorefxn.yml ../slow_anneal.yml with_random_spacers.yml,OUTPUT_PREFIX=spacers/mh_6" sgrna_mc
qsub -t 1-100 -v "ADDAPT_ARGS=mh_7.yml ../scorefxn.yml ../slow_anneal.yml with_random_spacers.yml,OUTPUT_PREFIX=spacers/mh_7" sgrna_mc
