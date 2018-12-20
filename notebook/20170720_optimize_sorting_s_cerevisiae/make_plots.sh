#!/usr/bin/env zsh
set -euo pipefail
source ../fcm.sh

fcm_pdf scatter_plot \
    s_cerevisiae/20170720_venus_controls.yml 'apo (17h)' \
    --output-size 8x11 \
    --cell-alpha 1.0



