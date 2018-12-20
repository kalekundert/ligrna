#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

for gel in $(ls ../../data/gels/*.tif | grep 'd[0-9]' | egrep -v 'transcribe|4kb|100ms|cr21|pcr|clone|with_kianna'); do
    gel_slug=$(basename ${gel%.tif})
    analyzed='no'

    for dens in ../../data/densiometry/*.xlsx; do
        dens_slug=$(basename ${dens%.xlsx})
        [ $dens_slug = $gel_slug ] && analyzed='yes'
    done;

    if [ $analyzed = 'no' ]; then
        echo $(basename $gel)
    fi
done
