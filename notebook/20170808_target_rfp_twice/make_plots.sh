#!/usr/bin/env bash
set -euo pipefail

source ../fcm.sh

fcm fold_change 20170808_double_target_rfp.yml
fcm fold_change 20170826_double_target_rfp.yml -O8x10

