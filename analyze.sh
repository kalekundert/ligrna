#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

rm -rf figures/
mkdir -p figures/auto_corr figures/seq_logo

echo "Making autocorrelation plots..."
tools/auto_corr no_spacers/mh_6_001.tsv -w 1000    -o figures/auto_corr/mh_6_without_spacers.pdf
tools/auto_corr no_spacers/mh_7_001.tsv -w 1000    -o figures/auto_corr/mh_7_without_spacers.pdf
tools/auto_corr spacers/mh_6_001.tsv    -w 4000    -o figures/auto_corr/mh_6_with_spacers.pdf
tools/auto_corr spacers/mh_7_001.tsv    -w 4000    -o figures/auto_corr/mh_7_with_spacers.pdf

echo "Making sequence logos..."
tools/seq_logo  no_spacers/mh_6_???.tsv -w 600  -i -o figures/seq_logo/mh_6_without_spacers.pdf
tools/seq_logo  no_spacers/mh_7_???.tsv -w 600  -i -o figures/seq_logo/mh_7_without_spacers.pdf
tools/seq_logo  spacers/mh_6_???.tsv    -w 2000 -i -o figures/seq_logo/mh_6_with_spacers.pdf
tools/seq_logo  spacers/mh_7_???.tsv    -w 2000 -i -o figures/seq_logo/mh_7_with_spacers.pdf
