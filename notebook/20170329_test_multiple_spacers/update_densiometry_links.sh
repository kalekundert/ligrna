#!/usr/bin/env bash
set -euo pipefail

for xlsx in $(ls ../../data/densiometry/*.xlsx | grep 'd[0-9]'); do
    if [ ! -e densiometry/$(basename $xlsx) ]; then
        echo $(basename $xlsx)
        ln -s ../$xlsx densiometry
    fi
done

