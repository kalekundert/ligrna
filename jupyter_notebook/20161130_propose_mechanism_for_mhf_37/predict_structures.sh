#!/usr/bin/env bash
set -euo pipefail

sgrna_sensor -rc -C "always"    \
    mhf/37                      \
    gfp/mhf/37                  \
    rfp/mhf/37                  \
    gfp2/mhf/37                 \
    rfp2/mhf/37                 \
    > mhf_37.less


