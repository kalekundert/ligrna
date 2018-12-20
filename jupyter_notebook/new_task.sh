#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if [ $# != 1 ]; then
    echo "Usage: new_task.sh <name>"
    exit 1
fi

proj=$(\date +%Y%m%d)_$1

mkdir $proj
ln -nsf $proj current
echo $proj

