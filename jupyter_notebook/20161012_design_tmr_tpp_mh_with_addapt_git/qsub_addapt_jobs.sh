#!/usr/bin/env sh
set -euo pipefail

constructs="tmr_hairpin_insertion tpp_hairpin_insertion"
scorefxns="not_active misfold_nexus"

for construct in $constructs; do
for scorefxn in $scorefxns; do

echo qsub -t 1-25 -v "\
ADDAPT_ARGS=\
inputs/constructs/$construct.yml \
inputs/scorefxns/$scorefxn.yml \
inputs/spacers/random.yml \
inputs/thermostats/auto_anneal.yml \
-n10000,\
OUTPUT_PREFIX=\
results/$construct/$scorefxn" sgrna_mc

done
done
