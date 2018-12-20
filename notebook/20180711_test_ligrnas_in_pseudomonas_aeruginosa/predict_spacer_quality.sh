#!/usr/bin/env bash

cd ../20170329_test_multiple_spacers
for x in fol{1..20}; do
    echo $x
    python3.6 predict_spacer_quality.py $x 'rxb 11,1'
    echo
done
