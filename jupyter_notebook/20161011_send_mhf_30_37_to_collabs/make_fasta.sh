#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

fasta_path='20161011_best_designs.fa'
../../scripts/show_seqs.py -Sf mhf/30 mhf/37 > $fasta_path
sed -i 's/None\///g' $fasta_path

