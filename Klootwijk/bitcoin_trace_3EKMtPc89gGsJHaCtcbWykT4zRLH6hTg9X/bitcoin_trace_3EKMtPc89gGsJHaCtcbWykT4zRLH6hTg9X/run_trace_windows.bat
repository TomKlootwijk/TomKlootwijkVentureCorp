@echo off
python -m pip install -r requirements.txt
python trace_bitcoin.py --address 3EKMtPc89gGsJHaCtcbWykT4zRLH6hTg9X --from-date 2020-01-01 --to-date 2020-12-31 --out live_trace
pause
