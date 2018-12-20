#!/usr/bin/env bash
set -euo pipefail
source ../fcm.sh

fcm fold_change 20180725_test_b_subtilis.yml
fcm fold_change 20180731_b_subtilis_theo_titration.yml


