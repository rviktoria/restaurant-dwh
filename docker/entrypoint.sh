#!/bin/bash

# Run main.py
python main.py || exit 1
echo "cron time"
# Start cron service in the background
cron -f
