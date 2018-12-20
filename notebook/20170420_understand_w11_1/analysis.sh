#!/usr/bin/env bash
set -euxo pipefail
FCM=../../flow_cytometry

$FCM/fold_change.py \
    $FCM/data/20170420_repeat_w11_1.yml \
    -o $.svg

$FCM/fold_change.py \
    $FCM/data/20170502_won_w11_1.yml \
    -o $.svg
