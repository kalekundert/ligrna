#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

#rm -rf figures/mh_design
mkdir -p figures/mh_design/{no,example,random}_spacers/{auto_corr,pick_seqs,seq_logo}

#echo "Making autocorrelation plots..."
#tools/auto_corr results/no_spacers/mh_6_001.tsv      -w 2000 -o figures/mh_design/no_spacers/auto_corr/mh_6.pdf
#tools/auto_corr results/no_spacers/mh_7_001.tsv      -w 2000 -o figures/mh_design/no_spacers/auto_corr/mh_7.pdf
#tools/auto_corr results/example_spacers/mh_6_001.tsv -w 2000 -o figures/mh_design/example_spacers/auto_corr/mh_6.pdf
#tools/auto_corr results/example_spacers/mh_7_001.tsv -w 2000 -o figures/mh_design/example_spacers/auto_corr/mh_7.pdf
#tools/auto_corr results/random_spacers/mh_6_001.tsv  -w 2000 -o figures/mh_design/random_spacers/auto_corr/mh_6.pdf
#tools/auto_corr results/random_spacers/mh_7_001.tsv  -w 2000 -o figures/mh_design/random_spacers/auto_corr/mh_7.pdf

echo "Picking sequences..."
tools/pick_seqs results/no_spacers/mh_6_???.tsv      -w 500 -vv -s > figures/mh_design/no_spacers/pick_seqs/mh_6.pdf
tools/pick_seqs results/no_spacers/mh_7_???.tsv      -w 500 -vv -s > figures/mh_design/no_spacers/pick_seqs/mh_7.pdf
tools/pick_seqs results/example_spacers/mh_6_???.tsv -w 500 -vv -s > figures/mh_design/example_spacers/pick_seqs/mh_6.pdf
tools/pick_seqs results/example_spacers/mh_7_???.tsv -w 500 -vv -s > figures/mh_design/example_spacers/pick_seqs/mh_7.pdf
tools/pick_seqs results/random_spacers/mh_6_???.tsv  -w 500 -vv -s > figures/mh_design/random_spacers/pick_seqs/mh_6.pdf
tools/pick_seqs results/random_spacers/mh_7_???.tsv  -w 500 -vv -s > figures/mh_design/random_spacers/pick_seqs/mh_7.pdf

#echo "Making sequence logos..."
#tools/seq_logo results/no_spacers/mh_6_???.tsv      -w 500 -i -o figures/mh_design/no_spacers/seq_logo/mh_6.pdf
#tools/seq_logo results/no_spacers/mh_7_???.tsv      -w 500 -i -o figures/mh_design/no_spacers/seq_logo/mh_7.pdf
#tools/seq_logo results/example_spacers/mh_6_???.tsv -w 500 -i -o figures/mh_design/example_spacers/seq_logo/mh_6.pdf
#tools/seq_logo results/example_spacers/mh_7_???.tsv -w 500 -i -o figures/mh_design/example_spacers/seq_logo/mh_7.pdf
#tools/seq_logo results/random_spacers/mh_6_???.tsv  -w 500 -i -o figures/mh_design/random_spacers/seq_logo/mh_6.pdf
#tools/seq_logo results/random_spacers/mh_7_???.tsv  -w 500 -i -o figures/mh_design/random_spacers/seq_logo/mh_7.pdf
