#!/bin/bash

# Run admin bot in the background
node /ctf/admin_bot.js &

# Run Flask server on port 80 (foreground)
python3 /ctf/app.py
