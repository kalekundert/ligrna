#!/usr/bin/env bash
set -euo pipefail

./clone_into_sgrna.py $@            \
    'mhf/4 -b mhf/4/1 -s gfp'       \
    'mhf/4 -b mhf/4/1 -s gfp2'      \
    'mhf/4 -b mhf/4/1 -s rfp'       \
    'mhf/4 -b mhf/4/1 -s rfp2'      \
                                    \
    'mhf/7 -b mhf/7/1 -s gfp'       \
    'mhf/7 -b mhf/7/1 -s gfp2'      \
    'mhf/7 -b mhf/7/1 -s rfp'       \
    'mhf/7 -b mhf/7/1 -s rfp2'      \
                                    \
    'mhf/13 -b mhf/13/1 -s gfp'     \
    'mhf/13 -b mhf/13/1 -s gfp2'    \
    'mhf/13 -b mhf/13/1 -s rfp'     \
    'mhf/13 -b mhf/13/1 -s rfp2'    \
                                    \
    'mhf/21 -b mhf/21/1'            \
                                    \
    'mhf/26 -b mhf/26/1'            \
                                    \
    'mhf/35 -b mhf/35/1 -s gfp'     \
    'mhf/35 -b mhf/35/1 -s gfp2'    \
    'mhf/35 -b mhf/35/1 -s rfp'     \
    'mhf/35 -b mhf/35/1 -s rfp2'    \
                                    \
    'mhf/37 -b mhf/37/1 -s gfp'     \
    'mhf/37 -b mhf/37/1 -s gfp2'    \
    'mhf/37 -b mhf/37/1 -s rfp'     \
    'mhf/37 -b mhf/37/1 -s rfp2'    \
                                    \
    'mhf/38 -b mhf/38/1 -s gfp'     \
    'mhf/38 -b mhf/38/1 -s gfp2'    \
    'mhf/38 -b mhf/38/1 -s rfp'     \
    'mhf/38 -b mhf/38/1 -s rfp2'    \
