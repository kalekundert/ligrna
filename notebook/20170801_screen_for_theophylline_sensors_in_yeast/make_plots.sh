#!/usr/bin/env bash
set -euo pipefail
source ../fcm.sh

fcm fold_change 20170913_screen_theo_ux.yml -d 1e-2,1e1
fcm fold_change 20171027_screen_theo_rhi.yml -d 1e-2,1e1

