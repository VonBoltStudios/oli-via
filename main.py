#!/usr/bin/env python3
"""Oli Voice Interaction App — main conversation loop."""

import sys
import yaml
from modules.audio import AudioCapture
from modules.wake_word import WakeWordDetector
from modules.stt import STT
from modules.llm import LLM
from modules.tts import TTS


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config()

    audio = AudioCapture(
        sample_rate=cfg["audio"]["sample_rate"],
        channels=cfg["audio"]["channels"],
        chunk_ms=cfg["audio"]["chunk_ms"],
    )
    wake = WakeWordDetector(
        phrase=cfg["wake_word"]["phrase"],
        threshold=cfg["wake_word"]["threshold"],
    )
    stt = STT(
        model_size=cfg["stt"]["model"],
        language=cfg["stt"]["language"],
        device=cfg["stt"]["device"],
        compute_type=cfg["stt"]["compute_type"],
    )
    llm = LLM(
        base_url=cfg["llm"]["base_url"],
        model=cfg["llm"]["model"],
        temperature=cfg["llm"]["temperature"],
        max_tokens=cfg["llm"]["max_tokens"],
        system_prompt=cfg["persona"]["system_prompt"],
    )
    tts = TTS(
        voice=cfg["tts"]["voice"],
        speed=cfg["tts"]["speed"],
        output_device=cfg["tts"].get("output_device"),
    )

    name = cfg["persona"]["name"]
    print(f"\n{name} is ready. Listening for wake word: '{cfg['wake_word']['phrase']}'\n")

    for audio_chunk in audio.stream():
        if not wake.check(audio_chunk):
            continue

        print(f"[wake word detected]")
        tts.speak(f"Yes, I'm here.")

        utterance_audio = audio.record_until_silence(
            silence_threshold_ms=cfg["audio"]["silence_threshold_ms"],
            max_record_s=cfg["audio"]["max_record_s"],
        )

        text = stt.transcribe(utterance_audio, sample_rate=cfg["audio"]["sample_rate"])
        if not text:
            print("  [no speech detected]")
            continue

        print(f"  You: {text}")

        reply = llm.chat(text)
        print(f"  {name}: {reply}")

        tts.speak(reply)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down.")
        sys.exit(0)
