#!/usr/bin/env bash
set -euo pipefail
source ../fcm.sh

fcm fold_change  20180725_sadcas9_spacer_test.yml
fcm scatter_plot 20180725_sadcas9_spacer_test.yml GFP -o '$_gfp.svg' -O 3x12
fcm scatter_plot 20180725_sadcas9_spacer_test.yml RFP -o '$_rfp.svg' -O 3x12

fcm fold_change  20180731_sadcas9_spacer_test.yml
fcm scatter_plot 20180731_sadcas9_spacer_test.yml GFP -o '$_gfp.svg' -O 3x12
fcm scatter_plot 20180731_sadcas9_spacer_test.yml RFP -o '$_rfp.svg' -O 3x12

fcm fold_change  20180802_sadcas9_atc_toxicity.yml -O 6x10

./growth_curve.py 20180802_sadcas9_atc_toxicity.toml

fcm fold_change 20180817_sadcas9_test_ligrnas.yml -O 6x9
