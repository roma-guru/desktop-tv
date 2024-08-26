#!/bin/bash
. .venv/bin/activate && python3 main.py &
ngrok http 8080
