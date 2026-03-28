#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate agent-dev

python scripts/watchdog_review.py
