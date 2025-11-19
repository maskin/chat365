import io
import os
from google.cloud import speech

# Ensure you have set GOOGLE_APPLICATION_CREDENTIALS environment variable
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

def transcribe_audio(audio_file_path):
    """Transcribes the given audio file."""
    client = speech.SpeechClient()

    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ja-JP",
        enable_automatic_punctuation=True,
    )

    print(f"Transcribing {audio_file_path}...")
    try:
        response = client.recognize(config=config, audio=audio)

        for result in response.results:
            print("Transcript: {}".format(result.alternatives[0].transcript))
            
        if not response.results:
            print("No results returned.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # You need a sample audio file. 
    # For now, we'll check if one exists or ask the user to provide one, 
    # but this script assumes one is passed or hardcoded.
    # Let's try to find a dummy file or create one if possible, 
    # but creating a valid WAV file programmatically without external libs is hard.
    # We will assume a file named 'test_audio.wav' exists in the same directory for now.
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(current_dir, "test_audio.wav")
    
    if not os.path.exists(audio_path):
        print(f"Error: Test audio file not found at {audio_path}")
        print("Please place a 16kHz mono WAV file named 'test_audio.wav' in the tests directory.")
    else:
        transcribe_audio(audio_path)
