#!/usr/bin/env bash
set -euo pipefail

rsync -avz \
    sgrna_mc qsub_addapt_jobs.sh inputs \
    chef:sgrna/subprojects/20161012_design_tmr_tpp_mh_with_addapt
