#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

DATA=../../data/facs
BIN=../../flow_cytometry
OUTPUT=${1:-$.pdf}

$BIN/fold_change.py                                                     \
    $DATA/20171205_tpp_time_course.yml                                  \
    --output $OUTPUT                                                    \
    --output-size 8x10                                                  \
    --fold-change-xlim 2                                                \
    --normalize-by-internal-control                                     \
    --pdf                                                               \

$BIN/fold_change.py                                                     \
    $DATA/20171205_tpp_time_course_with_acgu.yml                        \
    --output $OUTPUT                                                    \
    --output-size 8x10                                                  \
    --fold-change-xlim 2                                                \
    --normalize-by-internal-control                                     \
    --pdf                                                               \

