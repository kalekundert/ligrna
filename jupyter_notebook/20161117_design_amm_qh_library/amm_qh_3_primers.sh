#!/usr/bin/env bash
set -euo pipefail

# With the default annealing temperature (60°C), I get one primer that's 51 bp 
# long, which makes it dramatically more expensive.  Lowering the annealing 
# temperature to 58°C makes that primer one nucleotide shorter.  The annealing 
# temperature recommended by the online NEB tool for these primers is still 
# 61°C.

~/sgrna/scripts/clone_into_sgrna.py amm/qh/3 -T 58 | tee amm_qh_3_primers.txt


