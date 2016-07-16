#!/usr/bin/env bash
set -euo pipefail

./scripts/mount_guybrush.sh || true &> /dev/null
rsync -avz chef:sgrna/addapt/results/ results
