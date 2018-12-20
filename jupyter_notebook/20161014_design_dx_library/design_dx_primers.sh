#!/usr/bin/env bash
set -euo pipefail

./clone_into_sgrna.py       \
    'rxb/11/1 -b on'        \
    'dx/9     -b rxb/11/1'  \
    | tee dx_primers.txt

