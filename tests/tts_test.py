"""
Text-to-Speech API 技術検証スクリプト
Google Cloud Text-to-Speech APIの動作確認
"""
import os
from google.cloud import texttospeech

# 環境変数からAPIキーのパスを取得
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TEXT_TO_SYNTHESIZE = "こんにちは。これは、Google Cloud Text-to-Speech APIのテストです。音声が正常に生成されているか確認してください。"
OUTPUT_FILE = "tests/output_ja.mp3"


def check_credentials():
    """認証情報の確認"""
    if not CREDENTIALS_PATH:
        print("❌ 環境変数 GOOGLE_APPLICATION_CREDENTIALS が設定されていません")
        print("設定方法:")
        print("  export GOOGLE_APPLICATION_CREDENTIALS='path/to/service-account-key.json'")
        return False
    
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"❌ 認証ファイルが見つかりません: {CREDENTIALS_PATH}")
        return False
    
    print(f"✅ 認証情報: {CREDENTIALS_PATH}")
    return True


def synthesize_text(text, output_filename):
    """テキストを音声に変換"""
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
        
        print(f"\n🔊 テキストを音声に変換中...")
        print(f"テキスト: {text[:50]}...")
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        with open(output_filename, "wb") as out:
            out.write(response.audio_content)
        
        print(f"\n✅ 音声ファイルを生成しました: {output_filename}")
        print(f"ファイルサイズ: {len(response.audio_content)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False




def play_audio(filename):
    """音声ファイルを再生する (macOS/Linux)"""
    import subprocess
    import platform
    
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            print(f"▶️ 再生中: {filename}")
            subprocess.run(["afplay", filename], check=True)
        elif system == "Linux":
            # Linux (aplay or mpg123) - 簡易的な実装
            subprocess.run(["aplay", filename], check=False)
        else:
            print("⚠️ このOSでの自動再生はサポートされていません")
            
    except Exception as e:
        print(f"⚠️ 再生中にエラーが発生しました: {e}")


def test_multiple_voices():
    """複数の音声タイプをテスト"""
    print("\n" + "=" * 60)
    print("複数音声タイプのテスト")
    print("=" * 60)
    
    voices = [
        ("NEUTRAL", texttospeech.SsmlVoiceGender.NEUTRAL),
        ("FEMALE", texttospeech.SsmlVoiceGender.FEMALE),
        ("MALE", texttospeech.SsmlVoiceGender.MALE),
    ]
    
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text="こんにちは")
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        for voice_name, gender in voices:
            voice = texttospeech.VoiceSelectionParams(
                language_code="ja-JP",
                ssml_gender=gender
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            filename = f"tests/output_ja_{voice_name.lower()}.mp3"
            with open(filename, "wb") as out:
                out.write(response.audio_content)
            
            print(f"✅ {voice_name}: {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def main():
    print("=" * 60)
    print("Google Cloud Text-to-Speech API 技術検証")
    print("=" * 60)
    
    # 認証確認
    if not check_credentials():
        print("\n⚠️  Google Cloudの設定が必要です")
        print("\n【セットアップ手順】")
        print("1. Google Cloud Consoleにアクセス")
        print("   https://console.cloud.google.com/")
        print("2. プロジェクトを作成（未作成の場合）")
        print("3. Text-to-Speech APIを有効化")
        print("4. サービスアカウントを作成してJSONキーをダウンロード")
        print("5. 環境変数を設定:")
        print("   export GOOGLE_APPLICATION_CREDENTIALS='path/to/key.json'")
        return
    
    # ディレクトリ作成
    os.makedirs("tests", exist_ok=True)
    
    # 基本的な音声合成テスト
    success = synthesize_text(TEXT_TO_SYNTHESIZE, OUTPUT_FILE)
    
    if success:
        # 音声を再生
        play_audio(OUTPUT_FILE)

        # 複数音声タイプのテスト
        test_multiple_voices()
        
        print("\n" + "=" * 60)
        print("✅ 技術検証: 成功")
        print("=" * 60)
        print("\n📢 生成された音声ファイルを再生して確認してください")
        print("   macOSの場合: open tests/output_ja.mp3")
    else:
        print("\n" + "=" * 60)
        print("❌ 技術検証: 失敗")
        print("=" * 60)


if __name__ == "__main__":
    main()
