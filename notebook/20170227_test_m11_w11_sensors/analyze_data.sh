#!/usr/bin/env bash
set -euo pipefail
source ../fcm.sh

#fcm fold_change 20170315_test_w11_m11.yml \
    #-o $.svg -O 7x9 -d 1e-3,1e1 -p -m mode 
    
fcm fold_change 20170315_test_w11_m11_condensed.yml \
    -o $.svg -O 7x6.5 -d 3e-3,4e0 -p -m mode 
    
