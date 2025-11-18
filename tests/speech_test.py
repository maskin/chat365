"""
Speech-to-Text API 技術検証スクリプト
Google Cloud Speech-to-Text APIの動作確認
"""
import io
import os
from google.cloud import speech

# 環境変数からAPIキーのパスを取得
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
AUDIO_FILE = "tests/test_audio_ja.wav"  # テスト用音声ファイル（要準備）


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


def transcribe_audio(audio_file_path):
    """音声ファイルをテキストに変換"""
    if not os.path.exists(audio_file_path):
        print(f"❌ 音声ファイルが見つかりません: {audio_file_path}")
        print("\n📝 テスト用音声ファイルの準備方法:")
        print("1. macOSの場合: QuickTime Playerで録音")
        print("2. 形式: WAV, 16000Hz, モノラル")
        print("3. 内容: 「こんにちは。これはテストです。」などの簡単な日本語")
        print(f"4. 保存先: {audio_file_path}")
        return None
    
    try:
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
        
        print(f"\n🎤 音声ファイル '{audio_file_path}' の文字起こしを開始...")
        response = client.recognize(config=config, audio=audio)
        
        if not response.results:
            print("❌ 音声が認識されませんでした")
            return None
        
        print("\n✅ 認識成功！\n")
        for i, result in enumerate(response.results):
            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence
            print(f"結果 {i+1}:")
            print(f"  テキスト: {transcript}")
            print(f"  信頼度: {confidence:.2%}")
        
        return response.results
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return None


def main():
    print("=" * 60)
    print("Google Cloud Speech-to-Text API 技術検証")
    print("=" * 60)
    
    # 認証確認
    if not check_credentials():
        print("\n⚠️  Google Cloudの設定が必要です")
        print("\n【セットアップ手順】")
        print("1. Google Cloud Consoleにアクセス")
        print("   https://console.cloud.google.com/")
        print("2. プロジェクトを作成（未作成の場合）")
        print("3. Speech-to-Text APIを有効化")
        print("4. サービスアカウントを作成してJSONキーをダウンロード")
        print("5. 環境変数を設定:")
        print("   export GOOGLE_APPLICATION_CREDENTIALS='path/to/key.json'")
        return
    
    # 音声認識テスト
    result = transcribe_audio(AUDIO_FILE)
    
    if result:
        print("\n" + "=" * 60)
        print("✅ 技術検証: 成功")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 技術検証: 失敗")
        print("=" * 60)


if __name__ == "__main__":
    main()
