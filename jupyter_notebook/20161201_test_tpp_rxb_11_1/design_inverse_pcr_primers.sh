#!/usr/bin/env bash
set -euo pipefail

# Lower the annealing temperature to keep both primers below 60 bp.
~/sgrna/scripts/clone_into_sgrna.py 'tpp/rxb/11/1' -T 54 | tee primers.txt
