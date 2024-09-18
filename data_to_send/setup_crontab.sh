#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

if ! command -v crontab &> /dev/null; then
    echo "Cron is not installed. Installing..."
    if [ -x "$(command -v apt)" ]; then
        sudo apt update -qq
        sudo apt install cron -y -qq
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install cronie -y
        sudo systemctl start crond
        sudo systemctl enable crond
    else
        echo "Unsupported package manager. Please install cron manually."
        exit 1
    fi
fi

if ! sudo systemctl is-active --quiet cron; then
    sudo systemctl start cron
    sudo systemctl enable cron
fi

SCRIPT_NAME="docker_checker.py"
SCRIPT_PATH=$(find ~ -type f -name "$SCRIPT_NAME" 2>/dev/null | head -n 1)

if [ -z "$SCRIPT_PATH" ]; then
    echo "Error: $SCRIPT_NAME not found."
    exit 1
fi

chmod +x "$SCRIPT_PATH"

CRON_JOB="*/3 * * * * python3 $SCRIPT_PATH"

(crontab -l | grep -F "$SCRIPT_PATH") >/dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "Cron job already exists. Skipping."
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully."
fi
