#!/usr/bin/env bash
set -uo pipefail
IFS=$'\n\t'

mkdir -p figures/param_opt/auto_anneal_{25,50,75}/{no,example,random}_spacers
mkdir -p figures/param_opt/auto_{25,50,75}/{no,example,random}_spacers

echo "Picking sequences..."
echo "Auto Scale 25%, No Spacers"                                                  > figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_25/no_spacers/mh_???.tsv             -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 50%, No Spacers"                                                  >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_50/no_spacers/mh_???.tsv             -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 75%, No Spacers"                                                  >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_75/no_spacers/mh_???.tsv             -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 25%, No Spacers"                                                 >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_25/no_spacers/mh_???.tsv      -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 50%, No Spacers"                                                 >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_50/no_spacers/mh_???.tsv      -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 75%, No Spacers"                                                 >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_75/no_spacers/mh_???.tsv      -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 25%, Example Spacers"                                             >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_25/example_spacers/mh_???.tsv        -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 50%, Example Spacers"                                             >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_50/example_spacers/mh_???.tsv        -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 75%, Example Spacers"                                             >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_75/example_spacers/mh_???.tsv        -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 25%, Example Spacers"                                            >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_25/example_spacers/mh_???.tsv -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 50%, Example Spacers"                                            >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_50/example_spacers/mh_???.tsv -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 75%, Example Spacers"                                            >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_75/example_spacers/mh_???.tsv -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 25%, Random Spacers"                                              >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_25/random_spacers/mh_???.tsv         -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 50%, Random Spacers"                                              >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_50/random_spacers/mh_???.tsv         -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Scale 75%, Random Spacers"                                              >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_75/random_spacers/mh_???.tsv         -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 25%, Random Spacers"                                             >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_25/random_spacers/mh_???.tsv  -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 50%, Random Spacers"                                             >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_50/random_spacers/mh_???.tsv  -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt
echo "Auto Anneal 75%, Random Spacers"                                             >> figures/param_opt/pick_seqs.txt
tools/pick_seqs results/param_opt/auto_anneal_75/random_spacers/mh_???.tsv  -w 500 >> figures/param_opt/pick_seqs.txt
echo                                                                               >> figures/param_opt/pick_seqs.txt

echo "Making autocorrelation plots..."
tools/auto_corr results/param_opt/auto_anneal_25/no_spacers/mh_001.tsv      -w 1000 -o figures/param_opt/auto_anneal_25/no_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_25/example_spacers/mh_001.tsv -w 1000 -o figures/param_opt/auto_anneal_25/example_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_25/random_spacers/mh_001.tsv  -w 1000 -o figures/param_opt/auto_anneal_25/random_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_50/no_spacers/mh_001.tsv      -w 1000 -o figures/param_opt/auto_anneal_50/no_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_50/example_spacers/mh_001.tsv -w 1000 -o figures/param_opt/auto_anneal_50/example_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_50/random_spacers/mh_001.tsv  -w 1000 -o figures/param_opt/auto_anneal_50/random_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_75/no_spacers/mh_001.tsv      -w 1000 -o figures/param_opt/auto_anneal_75/no_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_75/example_spacers/mh_001.tsv -w 1000 -o figures/param_opt/auto_anneal_75/example_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_anneal_75/random_spacers/mh_001.tsv  -w 1000 -o figures/param_opt/auto_anneal_75/random_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_25/no_spacers/mh_001.tsv             -w 1000 -o figures/param_opt/auto_25/no_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_25/example_spacers/mh_001.tsv        -w 1000 -o figures/param_opt/auto_25/example_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_25/random_spacers/mh_001.tsv         -w 1000 -o figures/param_opt/auto_25/random_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_50/no_spacers/mh_001.tsv             -w 1000 -o figures/param_opt/auto_50/no_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_50/example_spacers/mh_001.tsv        -w 1000 -o figures/param_opt/auto_50/example_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_50/random_spacers/mh_001.tsv         -w 1000 -o figures/param_opt/auto_50/random_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_75/no_spacers/mh_001.tsv             -w 1000 -o figures/param_opt/auto_75/no_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_75/example_spacers/mh_001.tsv        -w 1000 -o figures/param_opt/auto_75/example_spacers/auto_corr.pdf
tools/auto_corr results/param_opt/auto_75/random_spacers/mh_001.tsv         -w 1000 -o figures/param_opt/auto_75/random_spacers/auto_corr.pdf

echo "Making sequence logos..."
tools/seq_logo results/param_opt/auto_anneal_25/no_spacers/mh_???.tsv      -i -w 500 -o figures/param_opt/auto_anneal_25/no_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_25/example_spacers/mh_???.tsv -i -w 500 -o figures/param_opt/auto_anneal_25/example_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_25/random_spacers/mh_???.tsv  -i -w 500 -o figures/param_opt/auto_anneal_25/random_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_50/no_spacers/mh_???.tsv      -i -w 500 -o figures/param_opt/auto_anneal_50/no_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_50/example_spacers/mh_???.tsv -i -w 500 -o figures/param_opt/auto_anneal_50/example_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_50/random_spacers/mh_???.tsv  -i -w 500 -o figures/param_opt/auto_anneal_50/random_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_75/no_spacers/mh_???.tsv      -i -w 500 -o figures/param_opt/auto_anneal_75/no_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_75/example_spacers/mh_???.tsv -i -w 500 -o figures/param_opt/auto_anneal_75/example_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_anneal_75/random_spacers/mh_???.tsv  -i -w 500 -o figures/param_opt/auto_anneal_75/random_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_25/no_spacers/mh_???.tsv             -i -w 500 -o figures/param_opt/auto_25/no_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_25/example_spacers/mh_???.tsv        -i -w 500 -o figures/param_opt/auto_25/example_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_25/random_spacers/mh_???.tsv         -i -w 500 -o figures/param_opt/auto_25/random_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_50/no_spacers/mh_???.tsv             -i -w 500 -o figures/param_opt/auto_50/no_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_50/example_spacers/mh_???.tsv        -i -w 500 -o figures/param_opt/auto_50/example_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_50/random_spacers/mh_???.tsv         -i -w 500 -o figures/param_opt/auto_50/random_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_75/no_spacers/mh_???.tsv             -i -w 500 -o figures/param_opt/auto_75/no_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_75/example_spacers/mh_???.tsv        -i -w 500 -o figures/param_opt/auto_75/example_spacers/seq_logo.pdf
tools/seq_logo results/param_opt/auto_75/random_spacers/mh_???.tsv         -i -w 500 -o figures/param_opt/auto_75/random_spacers/seq_logo.pdf
