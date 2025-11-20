import os
import subprocess
import platform
from google.cloud import texttospeech
import logging

logger = logging.getLogger(__name__)

def generate_audio(text: str, output_filename: str) -> bool:
    """
    Google Cloud TTSを使用してテキストから音声を生成する
    """
    try:
        client = texttospeech.TextToSpeechClient()
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # 音声設定: 日本語、ニュートラル
        voice = texttospeech.VoiceSelectionParams(
            language_code="ja-JP",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        logger.info(f"Generating audio for text: {text[:50]}...")
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # ディレクトリが存在することを確認
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        
        logger.info(f"Audio file generated: {output_filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        return False

def play_audio(filename: str) -> bool:
    """
    音声ファイルを再生する (macOS/Linux)
    """
    system = platform.system()
    
    try:
        if not os.path.exists(filename):
            logger.error(f"Audio file not found: {filename}")
            return False

        logger.info(f"Playing audio: {filename}")
        
        if system == "Darwin":  # macOS
            subprocess.run(["afplay", filename], check=True)
        elif system == "Linux":
            # Linux (aplay or mpg123)
            subprocess.run(["aplay", filename], check=False)
        else:
            logger.warning("Auto-play not supported on this OS")
            return False
            
        return True
            
    except Exception as e:
        logger.error(f"Error playing audio: {e}")
        return False
