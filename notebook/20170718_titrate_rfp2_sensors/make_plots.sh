#!/usr/bin/env bash
set -euo pipefail

source ../fcm.sh

fcm titration_curve 20170718_titrate_rfp2.yml    # noisy
fcm titration_curve 20170719_titrate_rfp2.yml    # no response to ligand
fcm fold_change 20170720_test_new_media.yml      # new media is ok
fcm fold_change 20170804_titrate_rfp2.yml -q rxb # LB, left plastic on, forgot aTC, populations very bimodal.
fcm events_per_sec 20170805_titrate_rfp2.yml on  # LB no mistakes, cells didn't grow evenly.
fcm titration_curve 20170807_titrate_rfp2.yml    # EZ, 24-well block.


