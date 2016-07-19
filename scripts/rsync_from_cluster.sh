#!/usr/bin/env bash
set -euo pipefail

[ $(hostname) != guybrush ] && ./scripts/mount_guybrush.sh &> /dev/null || true
rsync -avz chef:sgrna/addapt/results/ results
