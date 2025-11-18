# API技術検証計画書

## 1. 目的

本プロジェクトのコア技術である Google Cloud Speech-to-Text API および Text-to-Speech API が、
要件（特に日本語の扱いや性能）を満たすかを確認し、技術的リスクを早期に特定・軽減する。

## 2. 検証項目

1.  **認証とセットアップ:**
    - Google CloudプロジェクトでのAPI有効化とサービスアカウントキー（JSON）の取得が問題なく行えるか。
    - Python環境で、`pip install google-cloud-speech google-cloud-texttospeech` を用いたライブラリのインストールが正常に完了するか。
    - 環境変数 `GOOGLE_APPLICATION_CREDENTIALS` を用いた認証が正常に機能するか。

2.  **Speech-to-Text API (音声→テキスト):**
    - **入力:** 短い日本語の音声ファイル（WAV, 16000Hz, LINEAR16）。
    - **処理:** PythonスクリプトからAPIを呼び出し、音声ファイルをテキストに変換する。
    - **期待される結果:** 意味の通る日本語の文章が返却される。句読点もある程度正確に付与される。

3.  **Text-to-Speech API (テキスト→音声):**
    - **入力:** 簡単な日本語のテキスト文章。
    - **処理:** PythonスクリプトからAPIを呼び出し、テキストを音声ファイル（MP3）に変換する。
    - **期待される結果:** 自然で聞き取りやすい日本語の音声ファイルが生成される。イントネーションや読み方が不自然でないかを確認する。

## 3. 検証手順

1.  Google Cloud Consoleでサービスアカウントキーを取得し、ローカルに保存する。
2.  `GOOGLE_APPLICATION_CREDENTIALS` 環境変数を設定する。
3.  Pythonの仮想環境を作成し、必要なライブラリをインストールする。
4.  下記のサンプルコードを実行し、各APIの動作を確認する。

## 4. サンプルコード

### 4.1. Speech-to-Text サンプル

```python
# speech_test.py
import io
from google.cloud import speech

# 事前に "test_audio_ja.wav" のような音声ファイルを用意する
AUDIO_FILE = "path/to/your/test_audio_ja.wav"

def transcribe_jp_audio(audio_file_path):
    client = speech.SpeechClient()

    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="ja-JP",  # 日本語を指定
        enable_automatic_punctuation=True, # 句読点の自動付与を有効化
    )

    print(f"音声ファイル {audio_file_path} の文字起こしを開始...")
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"認識結果: {result.alternatives[0].transcript}")

if __name__ == "__main__":
    transcribe_jp_audio(AUDIO_FILE)
```

### 4.2. Text-to-Speech サンプル

```python
# tts_test.py
from google.cloud import texttospeech

TEXT_TO_SYNTHESIZE = "こんにちは。これは、Google Cloud Text-to-Speech APIのテストです。"
OUTPUT_FILE = "output_ja.mp3"

def synthesize_jp_text(text, output_filename):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ja-JP",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'音声コンテンツをファイル "{output_filename}" に書き出しました。')

if __name__ == "__main__":
    synthesize_jp_text(TEXT_TO_SYNTHESIZE, OUTPUT_FILE)
```
