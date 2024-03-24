#!/bin/bash

LOG_FILE="/home/pi/Documents/datac-consumer/datac-consumer-0.0.0/datac_consumer_monitor.log"  # Change this to your desired log file path

while true; do

    # Get the current time for logging
    CHECK_TIME=$(date '+%Y-%m-%d %H:%M:%S')

    # Use pgrep to check if datac-consumer process is running
    # pgrep is more precise than ps | grep combination as it avoids false positives
    if pgrep -f "datac-consumer-0.0.0/.venv/bin/python3 src/main.py" > /dev/null; then
        echo "$CHECK_TIME - OK" >> "$LOG_FILE"
    else
        # Start the process using poetry
        nohup poetry run python3 src/main.py > datac-consumer.log 2>&1 </dev/null &
        echo "$CHECK_TIME - Started the process" >> "$LOG_FILE"
    fi

    # Wait for 30 seconds before checking again
    sleep 30
done