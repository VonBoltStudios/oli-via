"""Audio capture: streaming chunks for wake word, then VAD-gated recording."""

import time
import numpy as np
import sounddevice as sd


class AudioCapture:
    def __init__(self, sample_rate: int, channels: int, chunk_ms: int):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_frames = int(sample_rate * chunk_ms / 1000)

    def stream(self):
        """Yield audio chunks as float32 numpy arrays (for wake word processing)."""
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=self.chunk_frames,
        ) as stream:
            while True:
                chunk, _ = stream.read(self.chunk_frames)
                yield chunk.flatten()

    def record_until_silence(
        self,
        silence_threshold_ms: int,
        max_record_s: int,
        amplitude_threshold: float = 0.01,
    ) -> np.ndarray:
        """
        Record audio until silence is detected. Returns full utterance as int16 array.
        Uses amplitude-based VAD — simple and reliable for edge hardware.
        """
        chunk_frames = self.chunk_frames
        silence_frames_needed = int(
            self.sample_rate * silence_threshold_ms / 1000 / chunk_frames
        )
        max_chunks = int(self.sample_rate * max_record_s / chunk_frames)

        frames = []
        silent_chunks = 0

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=chunk_frames,
        ) as stream:
            print("  [listening...]")
            for _ in range(max_chunks):
                chunk, _ = stream.read(chunk_frames)
                chunk = chunk.flatten()
                frames.append(chunk)

                if np.abs(chunk).mean() < amplitude_threshold:
                    silent_chunks += 1
                    if silent_chunks >= silence_frames_needed:
                        break
                else:
                    silent_chunks = 0

        audio = np.concatenate(frames)
        return (audio * 32768).astype(np.int16)
