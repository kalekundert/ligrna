#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

./clone_into_sgrna.py           \
    '3mx/mhf/37 -b mhf/37'      \
    '3mx/mhf/30 -b mhf/30'      \
    '3mx/mhf/37 -b mhf/37 -q'   \
    '3mx/mhf/30 -b mhf/30 -q'   \
    | tee 3mx_primers.txt
