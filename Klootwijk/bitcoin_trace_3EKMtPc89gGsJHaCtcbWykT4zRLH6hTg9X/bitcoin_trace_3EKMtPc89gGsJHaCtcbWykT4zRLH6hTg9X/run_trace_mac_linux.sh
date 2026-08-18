#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -r requirements.txt
python3 trace_bitcoin.py --address 3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X --from-date 2020-01-01 --to-date 2020-12-31 --out live_trace
