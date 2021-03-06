#!/usr/bin/env bash
set -euo pipefail

# Manually set the cutpoints such that the forward primers contain the 
# randomized ruler and the reverse primers contain the randomized nexus, such 
# that all the primers can be mixed and matched.  I put the cutpoint on the 
# ruler side to minimize the chance that the nexus loop or U59 would be 
# truncated in some designs.

~/sgrna/scripts/clone_into_sgrna.py \
    'tpp/mhf/30 -b on'              \
    -b tpp/mhf/30                   \
    'tpp/uh/4/6 -c 7'               \
    'tpp/uh/4/7 -c 7'               \
    'tpp/uh/5/6 -c 8'               \
    'tpp/uh/5/7 -c 8'               \
    'tpp/uh/6/6 -c 9'               \
| tee raw_primers.txt


