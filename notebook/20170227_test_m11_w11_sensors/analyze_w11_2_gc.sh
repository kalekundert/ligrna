#!/usr/bin/env bash
set -euo pipefail

../../flow_cytometry/fold_change.py \
    ../../flow_cytometry/data/20170418_test_w11_2_gc.yml \
    -m mode -o $.svg
    
