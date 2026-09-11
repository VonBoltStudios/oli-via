#!/bin/bash
# Oli Voice Interaction App — launch script

set -e
cd "$(dirname "$0")"

# Add piper to PATH
export PATH="$HOME/.local/share/piper:$PATH"

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    ollama serve &>/dev/null &
    sleep 2
fi

# Activate venv and run
source .venv/bin/activate
python3 main.py
