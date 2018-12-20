#!/usr/bin/env bash
set -euo pipefail
../../scripts/design_mutagenesis_primers.py \
    KLEIN_TO_RAN \
    ttgacagctagctcagtcctaggtataatactagtaacatcaccatctaattcaacGTTTTAGTACTCTGTAATGAAAATTACAGAATCTACTAAAACAAGGCAAAATGCCGTGTTTATCTCGTCAACTTGTTGGCGAGA \
    ttgacagctagctcagtcctaggtataatactagtaacatcaccatctaattcaacGTTTTAGTACTCTGGAAACAGAATCTACTAAAACAAGGCAAAATGCCGTGTTTATCTCGTCAACTTGTTGGCGAGA \
    "$@"
