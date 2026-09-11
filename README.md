# Oli Voice Interaction App

A locally-running, end-to-end voice conversation system for the Oli humanoid robot. No cloud dependencies. All inference runs on the Jetson Orin NX.

## Requirements

- NVIDIA Jetson Orin NX, Ubuntu 22.04, aarch64
- CUDA drivers (JetPack — should be pre-installed)
- Internet connection for first-time model downloads only

## Installation

```bash
chmod +x install.sh start.sh
./install.sh
```

This will:
- Install Python dependencies
- Download and install Piper TTS (with default English voice)
- Install Ollama and pull the llama3.1:8b model (~4.5GB — takes a few minutes)

## Starting

```bash
./start.sh
```

Oli will start listening. Speak the wake word to trigger a conversation:

> **"Hey Oli"**

Oli will acknowledge, listen to your question, and respond aloud.

Press `Ctrl+C` to stop.

## Configuration

All settings are in `config.yaml`. You can change:

- **Wake word phrase** — the trigger phrase
- **Persona** — Oli's name, personality, and system prompt
- **STT model** — Whisper model size (trade off quality vs. speed)
- **LLM model** — Ollama model (swap to a different model if needed)
- **TTS voice** — Piper voice model
- **Audio thresholds** — silence detection sensitivity

No code changes needed — just edit `config.yaml` and restart.

## Troubleshooting

**Mic not working:** Check `sounddevice` can see your device: `python3 -c "import sounddevice; print(sounddevice.query_devices())"`

**Ollama not starting:** Run `ollama serve` manually in a terminal, then `./start.sh` in another.

**Wake word not triggering:** Lower `wake_word.threshold` in `config.yaml` (try 0.3).

**Response too slow:** Switch to a smaller STT model (`medium` instead of `large-v3`) or a smaller LLM.
