import os
from google.cloud import texttospeech

# Ensure you have set GOOGLE_APPLICATION_CREDENTIALS environment variable
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

def synthesize_text(text, output_filename):
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    print(f"Synthesizing text: '{text}'...")
    try:
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Audio content written to file "{output_filename}"')
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    text = "これは、Google Cloud Text-to-Speech APIのテストです。"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "output.mp3")
    
    synthesize_text(text, output_path)
