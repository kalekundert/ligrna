#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

mkdir -p figures/{mh_design,in_vitro}/{no,example,random}_spacers/{auto_corr,pick_seqs,seq_logo}

echo "Making autocorrelation plots..."
tools/auto_corr results/in_vitro/no_spacers/mh_7_001.tsv      -w 2000 -o figures/in_vitro/no_spacers/auto_corr/mh_7.pdf
tools/auto_corr results/in_vitro/example_spacers/mh_7_001.tsv -w 2000 -o figures/in_vitro/example_spacers/auto_corr/mh_7.pdf
tools/auto_corr results/in_vitro/random_spacers/mh_7_001.tsv  -w 2000 -o figures/in_vitro/random_spacers/auto_corr/mh_7.pdf

echo "Picking sequences..."
tools/pick_seqs results/in_vitro/no_spacers/mh_7_???.tsv      -w 500 -vv -s > figures/in_vitro/no_spacers/pick_seqs/mh_7.txt
tools/pick_seqs results/in_vitro/example_spacers/mh_7_???.tsv -w 500 -vv -s > figures/in_vitro/example_spacers/pick_seqs/mh_7.txt
tools/pick_seqs results/in_vitro/random_spacers/mh_7_???.tsv  -w 500 -vv -s > figures/in_vitro/random_spacers/pick_seqs/mh_7.txt

echo "Making sequence logos..."
tools/seq_logo results/in_vitro/no_spacers/mh_7_???.tsv      -w 500 -o figures/in_vitro/no_spacers/seq_logo/mh_7.pdf
tools/seq_logo results/in_vitro/example_spacers/mh_7_???.tsv -w 500 -o figures/in_vitro/example_spacers/seq_logo/mh_7.pdf
tools/seq_logo results/in_vitro/random_spacers/mh_7_???.tsv  -w 500 -o figures/in_vitro/random_spacers/seq_logo/mh_7.pdf
