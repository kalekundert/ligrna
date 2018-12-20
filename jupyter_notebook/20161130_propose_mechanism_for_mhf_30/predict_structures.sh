#!/usr/bin/env bash
set -euo pipefail

sgrna_sensor -rc -C "always"    \
    mhf/30                      \
    gfp/mhf/30                  \
    rfp/mhf/30                  \
    gfp2/mhf/30                 \
    rfp2/mhf/30                 \
    > mhf_30.less


