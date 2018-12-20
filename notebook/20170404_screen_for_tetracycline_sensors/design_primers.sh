#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

../../scripts/clone_into_sgrna.py   \
    tet/ux/3/2/g                    \
    tet/ux/4/3/g                    \
    tet/ux/5/4/g                    \
    "tet/rhi/4/4 -c9"               \
    "tet/rhi/4/5 -c9"               \
    "tet/rhi/5/4 -c10"              \
    "tet/rhi/5/5 -c10"              | tee primers.txt


