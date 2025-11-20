import wave
import sys

filename = "tests/test_audio.wav"

try:
    with wave.open(filename, "rb") as wf:
        print(f"File: {filename}")
        print(f"Channels: {wf.getnchannels()}")
        print(f"Sample width: {wf.getsampwidth()} bytes")
        print(f"Frame rate: {wf.getframerate()} Hz")
        print(f"Frames: {wf.getnframes()}")
        print(f"Duration: {wf.getnframes() / wf.getframerate():.2f} seconds")
except Exception as e:
    print(f"Error: {e}")
