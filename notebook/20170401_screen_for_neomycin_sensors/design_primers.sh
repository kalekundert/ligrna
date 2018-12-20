#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

../../scripts/clone_into_sgrna.py   \
    neo/ux/3/2/g                    \
    neo/ux/4/3/g                    \
    neo/ux/5/4/g                    \
    "neo/rhi/4/4 -c9"               \
    "neo/rhi/4/5 -c9"               \
    "neo/rhi/5/4 -c10"              \
    "neo/rhi/5/5 -c10"              | tee primers.txt


