#!/bin/bash
set -e

APP_DIR=~/CS4800-Assignment-2
LOG_FILE="$APP_DIR/log.txt"

cd "$APP_DIR"

git pull --rebase

pip3 install -r requirements.txt

pkill -f "python3 app.py" || true
sleep 1

nohup python3 app.py > "$LOG_FILE" 2>&1 &

echo "App restarted with PID $!"
