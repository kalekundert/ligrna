#!/usr/bin/env bash
set -euo pipefail

PATH=../../flow_cytometry:$PATH
fold_change.py \
    ../../data/facs/20161221_screen_amm_uh.yml  \
    -o $.pdf
