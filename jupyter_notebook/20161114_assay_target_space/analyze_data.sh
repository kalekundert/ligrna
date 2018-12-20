#!/usr/bin/env bash
set -euxo pipefail

fcm=../../flow_cytometry
$fcm/fold_change.py $fcm/data/20170111_test_n20_constructs.yml -o '$.svg'



