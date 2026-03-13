#!/bin/bash

# Configuration Variables
LOG_DIR="/var/log"
TARGET_LOG="$LOG_DIR/syslog" # Change to auth.log or your custom app log if needed
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
REPORT_FILE="error_report_$TIMESTAMP.txt"
TEMP_LOG="temp_filtered_log.txt"

echo "Initializing Log Analyzer Pipeline..."
echo "Targeting: $TARGET_LOG"

# Step 1: Pre-filter logs using grep to only grab relevant lines (speeds up Python processing)
# Requires sudo if accessing strict /var/log/ files
sudo grep -iE "error|failed|critical" "$TARGET_LOG" > "$TEMP_LOG"

# Step 2: Pass the filtered data to the Python script
echo "Parsing logs and identifying patterns..."
python3 log_analyzer.py "$TEMP_LOG" > "$REPORT_FILE"

# Step 3: Cleanup and Exit
rm "$TEMP_LOG"
echo "Analysis complete. Report saved locally to: $REPORT_FILE"

# Display the report in the terminal
cat "$REPORT_FILE"