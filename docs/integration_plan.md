# Integrating TTS into Scheduler

## Goal
Enable the scheduler to actually generate and play audio when a broadcast task is triggered, replacing the current "simulation" logic.

## Proposed Changes

### Backend Structure
#### [NEW] [src/backend/services/tts_service.py](file:///Users/maskin/Library/CloudStorage/Dropbox/0.github/pai/src/backend/services/tts_service.py)
- Encapsulate Google Cloud TTS logic (from `tests/tts_test.py`).
- Implement `generate_audio(text, output_path)` function.
- Implement `play_audio(file_path)` function using `afplay` (macOS) / `aplay` (Linux).

### Scheduler Logic
#### [MODIFY] [src/backend/scheduler.py](file:///Users/maskin/Library/CloudStorage/Dropbox/0.github/pai/src/backend/scheduler.py)
- Import `tts_service`.
- In `execute_broadcast`:
    1. Generate MP3 file from `broadcast.content`.
    2. Play the generated MP3 file.
    3. Handle errors (e.g., API failure, playback failure).

## Verification Plan

### Automated Tests
- Use `tests/verify_scheduler.py`.
- **Expectation**: When the script runs, an actual voice should be heard from the speakers.

### Manual Verification
- Check logs for "Audio generated" and "Playing audio" messages.
