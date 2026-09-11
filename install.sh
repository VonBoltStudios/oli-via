#!/bin/bash
# Oli Voice Interaction App — installation script
# Target: NVIDIA Jetson Orin NX, Ubuntu 22.04, aarch64

set -e

echo "=== Oli VIA Installer ==="
echo "Platform: $(uname -m) | $(lsb_release -ds 2>/dev/null || echo 'unknown')"
echo ""

# --- System dependencies ---
echo "[1/5] Installing system dependencies..."
sudo apt-get update -q
sudo apt-get install -y -q \
    python3-pip \
    python3-venv \
    portaudio19-dev \
    libsndfile1 \
    wget \
    curl

# --- Python virtual environment ---
echo "[2/5] Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip -q
pip install -q \
    faster-whisper \
    openwakeword \
    ollama \
    sounddevice \
    soundfile \
    pyyaml \
    numpy

# --- Piper TTS ---
echo "[3/5] Installing Piper TTS..."
PIPER_VERSION="1.2.0"
ARCH="aarch64"
PIPER_DIR="$HOME/.local/share/piper"
mkdir -p "$PIPER_DIR"

if [ ! -f "$PIPER_DIR/piper" ]; then
    PIPER_URL="https://github.com/rhasspy/piper/releases/download/${PIPER_VERSION}/piper_${ARCH}.tar.gz"
    wget -q "$PIPER_URL" -O /tmp/piper.tar.gz
    tar -xzf /tmp/piper.tar.gz -C "$PIPER_DIR" --strip-components=1
    rm /tmp/piper.tar.gz
fi

# Add piper to PATH for this session
export PATH="$PIPER_DIR:$PATH"

# Download default voice if not present
VOICE_DIR="$PIPER_DIR/voices"
mkdir -p "$VOICE_DIR"
VOICE="en_US-lessac-medium"
if [ ! -f "$VOICE_DIR/${VOICE}.onnx" ]; then
    echo "  Downloading voice: $VOICE"
    wget -q "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/${VOICE}.onnx" \
        -O "$VOICE_DIR/${VOICE}.onnx"
    wget -q "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/${VOICE}.onnx.json" \
        -O "$VOICE_DIR/${VOICE}.onnx.json"
fi

# --- Ollama ---
echo "[4/5] Installing Ollama..."
if ! command -v ollama &>/dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
fi

echo "  Starting Ollama service..."
ollama serve &>/dev/null &
sleep 3

echo "  Pulling llama3.1:8b (this may take a while)..."
ollama pull llama3.1:8b

# --- Done ---
echo "[5/5] Setup complete."
echo ""
echo "To start Oli: ./start.sh"
echo "To configure: edit config.yaml"
