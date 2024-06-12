#!/bin/bash
. .venv/bin/activate && python3 main.py &
if [[ -z $1 ]]; then
    ngrok http 8080
else
    ngrok http --domain=$1 8080
fi
