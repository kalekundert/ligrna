#!/usr/bin/env bash
set -euo pipefail

sgrna_sensor -b     \
    aavs/on         \
    gfp/on          \
    cf1/on          \
    cf2/on          \
    cf3/on          \
    aavs/off        \
    gfp/off         \
    cf1/off         \
    cf2/off         \
    cf3/off         \
    | tee 20170111_order_control_sgrna.txt
