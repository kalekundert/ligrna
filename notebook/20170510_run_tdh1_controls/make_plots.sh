#!/usr/bin/env bash
set -euo pipefail

FCM=../../flow_cytometry/

$FCM/fold_change.py                                         \
    $FCM/data/s_cerevisiae/20170518_rfp_neo_controls.yml    \
    -q 8h                                                   \
    -o '$_8h.svg'                                           \

$FCM/fold_change.py                                         \
    $FCM/data/s_cerevisiae/20170518_rfp_neo_controls.yml    \
    -q 23h                                                  \
    -o '$_23h.svg'                                          \

$FCM/fold_change.py                                         \
    $FCM/data/s_cerevisiae/20170718_venus_controls.yml      \
    -f 30                                                   \
    -o '$.svg'                                              \

$FCM/fold_change.py                                         \
    $FCM/data/s_cerevisiae/20170720_venus_controls_24h.yml  \
    -f 30                                                   \
    -O 7x10                                                 \
    -o '$.svg'                                              \

$FCM/events_per_sec.py                                      \
    $FCM/data/s_cerevisiae/20170720_venus_controls_24h.yml  \
    -o '$_event_rate.svg'                                   \
