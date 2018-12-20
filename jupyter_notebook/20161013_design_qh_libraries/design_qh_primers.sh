#!/usr/bin/env bash
set -euo pipefail

./clone_into_sgrna.py   \
    tpp/qh/3            \
    tpp/qh/4            \
    -b on               \
    | tee qh_primers.txt

