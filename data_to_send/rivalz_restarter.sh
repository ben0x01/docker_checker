#!/bin/bash

SCREEN_SESSION_NAME="rivalz"
LOG_FILE="/var/log/node_monitor.log"

if ! command -v screen &> /dev/null; then
    echo "$(date) - Screen не установлен, устанавливаю его..." >> $LOG_FILE
    if [ -x "$(command -v apt)" ]; then
        sudo apt update
        sudo apt install screen -y
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install screen -y
    else
        echo "$(date) - Не удалось установить screen, отсутствует подходящий пакетный менеджер." >> $LOG_FILE
        exit 1
    fi
fi

if ! screen -list | grep -q "$SCREEN_SESSION_NAME"; then
    echo "$(date) - Нода не запущена, перезапускаю через screen..." >> $LOG_FILE

    screen -dmS $SCREEN_SESSION_NAME bash -c "rivalz run"

    echo "$(date) - Нода успешно запущена в новой сессии screen ($SCREEN_SESSION_NAME)." >> $LOG_FILE
else
    echo "$(date) - Нода работает нормально." >> $LOG_FILE
fi

CRON_JOB="0 * * * * /path_to_script/monitor_node.sh >> /var/log/node_monitor_cron.log 2>&1"
(crontab -l | grep -F "/path_to_script/monitor_node.sh") >/dev/null 2>&1

if [ $? -ne 0 ]; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "$(date) - Cron job добавлен успешно." >> $LOG_FILE
else
    echo "$(date) - Cron job уже существует." >> $LOG_FILE
fi
