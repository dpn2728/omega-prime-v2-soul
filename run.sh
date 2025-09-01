#!/bin/bash

# Go to the project directory
cd /home/kec20/omega-prime-v2-soul || exit

# Activate the virtual environment and run the main script
# We use the full path to ensure it works correctly with systemd
/home/kec20/omega-prime-v2-soul/venv/bin/python3 -u main.py
