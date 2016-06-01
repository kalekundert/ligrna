#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

i=$1

./show_seqs.py -rcv -C always rbf/$i -s gfp > rbf_$i.less
./show_seqs.py -rcv -C always rbf/$i -S >> rbf_$i.less

vim rbf_$i.less

aha < rbf_$i.less > rbf_$i.html

