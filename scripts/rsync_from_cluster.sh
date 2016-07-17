#!/usr/bin/env bash
set -euo pipefail

./scripts/mount_guybrush.sh &> /dev/null || true
rsync -avz chef:sgrna/addapt/results/ results
