#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# The hits do not categorically score better than the starting point for the 
# library, so I don't think this is a useful metric.

function score_hit () {
    echo '********************************************************************'
    echo $1
    echo -n 'score: '
    addapt_score scorefxn.yml spacers.yml $1
}

score_hit mh_6.yml
score_hit mh_7.yml
score_hit mhf_37.yml
score_hit mhf_38.yml
score_hit mhf_25.yml
score_hit mhf_41.yml

