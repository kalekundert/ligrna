#!/usr/bin/env bash
set -euo pipefail
source ../fcm.sh

fcm bar_chart 20170920_rfp2_mhf_30_theo_3mx.yml
fcm fold_change 20170920_rfp2_mhf_30_theo_3mx.yml -o '$_fold_change.svg'

vienna theo_mhf_30 3mx_mhf_30 
