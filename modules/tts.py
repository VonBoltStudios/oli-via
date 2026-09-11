"""Text-to-speech via Piper TTS."""

import subprocess
import tempfile
import os
import sounddevice as sd
import soundfile as sf


class TTS:
    def __init__(self, voice: str, speed: float, output_device=None):
        self.voice = voice
        self.speed = speed
        self.output_device = output_device
        print(f"[TTS] Using Piper voice: {voice}")

    def speak(self, text: str):
        """Synthesize text and play audio via speaker."""
        if not text:
            return

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav_path = f.name

        try:
            # Piper CLI: echo "text" | piper --model <voice> --output_file out.wav
            subprocess.run(
                [
                    "piper",
                    "--model", self.voice,
                    "--output_file", wav_path,
                    "--length_scale", str(1.0 / self.speed),
                ],
                input=text.encode(),
                check=True,
                capture_output=True,
            )

            data, sample_rate = sf.read(wav_path)
            sd.play(data, sample_rate, device=self.output_device)
            sd.wait()

        finally:
            if os.path.exists(wav_path):
                os.unlink(wav_path)
