#!/usr/bin/env bash
set -euo pipefail

rsync -avz \
    chef:sgrna/subprojects/20161012_design_tmr_tpp_mh_with_addapt/results/ \
    results

