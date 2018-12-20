#!/usr/bin/env bash
set -euo pipefail

constructs="tmr_hairpin_insertion tpp_hairpin_insertion"
scorefxns="not_active misfold_nexus"

for construct in $constructs; do
for scorefxn in $scorefxns; do

echo "$construct ($scorefxn)..."
mkdir -p figures/$construct/$scorefxn

tools/plot_traj                                     \
    results/$construct/$scorefxn/traj_009.tsv       \
    -w 500                                          \
    -o figures/$construct/$scorefxn/plot_traj.pdf

tools/auto_corr                                     \
    results/$construct/$scorefxn/traj_009.tsv       \
    -w 500                                          \
    -o figures/$construct/$scorefxn/auto_corr.pdf

tools/seq_logo                                      \
    results/$construct/$scorefxn/traj_???.tsv       \
    -w 500                                          \
    -o figures/$construct/$scorefxn/seq_logo.pdf

done
done
