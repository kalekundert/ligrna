#!/usr/bin/env bash
set -euo pipefail

~/sgrna/scripts/clone_into_sgrna.py     \
    -b 'pam/on'                         \
    'pam/off'                           \
    'pam/rxb/11/1'                      \
    'pam/mhf/30'                        \
    'pam/mhf/37 -s aavs'                | tee mutate_sgrna.txt

