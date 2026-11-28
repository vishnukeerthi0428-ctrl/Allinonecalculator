#!/usr/bin/env bash
# Group R11 / letter L pipeline (Part 11.12). Deterministic: PYTHONHASHSEED=0.
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"
export PYTHONHASHSEED=0
python3 "$D/L_00_integrity.py"
python3 "$D/L_01_build_refs.py"
python3 "$D/L_02_inventory.py"
python3 "$D/L_03_compare.py"
python3 "$D/L_04_cluster.py"
python3 "$D/L_05_classify.py"
python3 "$D/L_06_coverage.py"
