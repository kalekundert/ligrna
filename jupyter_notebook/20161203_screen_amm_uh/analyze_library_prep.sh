#!/usr/bin/env bash
set -euo pipefail

../../scripts/unique_variants.py \
    ../../scripts/screens/amm_uh.yml \
    | tee library_prep.txt
