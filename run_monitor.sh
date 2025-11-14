#!/bin/bash
# --- Simple automation to run the monitor every 5 minutes ---

while true
do
    echo "--- Running Stock Check at $(date) ---"
    python3 stock_monitor.py
    echo "---------------------------------------"
    # Wait for 300 seconds (5 minutes)
    sleep 300 
done