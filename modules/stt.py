"""Speech-to-text via faster-whisper."""

import numpy as np
from faster_whisper import WhisperModel


class STT:
    def __init__(self, model_size: str, language: str, device: str, compute_type: str):
        self.language = language
        print(f"[STT] Loading Whisper {model_size} on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("[STT] Ready.")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        """Transcribe int16 audio array to text."""
        # faster-whisper expects float32 normalized to [-1, 1]
        audio_f32 = audio.astype(np.float32) / 32768.0
        segments, _ = self.model.transcribe(
            audio_f32,
            language=self.language,
            beam_size=5,
            vad_filter=True,           # built-in silero VAD to strip silence
        )
        return " ".join(seg.text.strip() for seg in segments).strip()
