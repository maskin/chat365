# セットアップガイド

このガイドでは、音声放送制御アプリの開発環境をセットアップする手順を説明します。

## 1. 前提条件

- **Python**: 3.9以上
- **Git**: 最新版
- **Google Cloudアカウント**: 有効な支払い方法が登録されていること（無料枠内で利用可能）

---

## 2. Google Cloud プロジェクトのセットアップ

### 2.1 プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 右上の「プロジェクトを選択」→「新しいプロジェクト」をクリック
3. プロジェクト名を入力（例: `chat365-broadcast`）
4. 「作成」をクリック

### 2.2 APIの有効化

#### Speech-to-Text APIの有効化
1. 左側メニューから「APIとサービス」→「ライブラリ」を選択
2. 検索バーに「Speech-to-Text」と入力
3. 「Cloud Speech-to-Text API」を選択
4. 「有効にする」をクリック

#### Text-to-Speech APIの有効化
1. 検索バーに「Text-to-Speech」と入力
2. 「Cloud Text-to-Speech API」を選択
3. 「有効にする」をクリック

### 2.3 サービスアカウントの作成

1. 左側メニューから「IAMと管理」→「サービスアカウント」を選択
2. 「サービスアカウントを作成」をクリック
3. サービスアカウント名を入力（例: `chat365-service-account`）
4. 「作成して続行」をクリック
5. ロールを選択:
   - 「Cloud Speech 管理者」
   - 「Cloud Text-to-Speech 管理者」
6. 「続行」→「完了」をクリック

### 2.4 認証キーのダウンロード

1. 作成したサービスアカウントをクリック
2. 「キー」タブを選択
3. 「鍵を追加」→「新しい鍵を作成」をクリック
4. キーのタイプ: JSON
5. 「作成」をクリック
6. JSONファイルが自動ダウンロードされる（例: `chat365-service-account-key.json`）

⚠️ **重要**: このJSONファイルは機密情報です。Gitリポジトリにコミットしないでください！

### 2.5 認証情報の配置

ダウンロードしたJSONファイルをプロジェクトディレクトリに配置します。

```bash
# プロジェクトルートに credentials ディレクトリを作成
mkdir -p credentials

# ダウンロードしたJSONファイルを移動
mv ~/Downloads/chat365-service-account-key.json credentials/
```

---

## 3. ローカル環境のセットアップ

### 3.1 リポジトリのクローン

```bash
git clone https://github.com/maskin/chat365.git
cd chat365
```

### 3.2 Python仮想環境の作成

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
# macOS/Linux:
source venv/bin/activate

# Windows:
# venv\Scripts\activate
```

### 3.3 依存パッケージのインストール

```bash
# pipのアップグレード
pip install --upgrade pip

# Google Cloud ライブラリのインストール
pip install google-cloud-speech google-cloud-texttospeech

# その他の必要なパッケージ
pip install apscheduler pygame pydub

# バックエンドの依存関係
pip install -r src/backend/requirements.txt
```

### 3.4 環境変数の設定

#### macOS/Linux

`~/.bashrc` または `~/.zshrc` に追加:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/chat365/credentials/chat365-service-account-key.json"
```

設定を反映:

```bash
source ~/.bashrc  # または source ~/.zshrc
```

#### Windows

PowerShellの場合:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\chat365\credentials\chat365-service-account-key.json"
```

永続的に設定する場合は「システムのプロパティ」→「環境変数」から設定してください。

---

## 4. 動作確認

### 4.1 環境変数の確認

```bash
echo $GOOGLE_APPLICATION_CREDENTIALS

# ファイルが存在するか確認
ls -l $GOOGLE_APPLICATION_CREDENTIALS
```

### 4.2 Speech-to-Text APIの動作確認

```bash
# テスト用音声ファイルの準備（まだの場合）
# macOSの場合: QuickTime Playerで録音
# 「こんにちは。これはテストです。」と録音
# 形式: WAV, 16000Hz
# 保存先: tests/test_audio_ja.wav

# テストスクリプト実行
python tests/speech_test.py
```

**期待される出力:**
```
============================================================
Google Cloud Speech-to-Text API 技術検証
============================================================
✅ 認証情報: /path/to/credentials/chat365-service-account-key.json

🎤 音声ファイル 'tests/test_audio_ja.wav' の文字起こしを開始...

✅ 認識成功！

結果 1:
  テキスト: こんにちは。これはテストです。
  信頼度: 95.23%

============================================================
✅ 技術検証: 成功
============================================================
```

### 4.3 Text-to-Speech APIの動作確認

```bash
python tests/tts_test.py
```

**期待される出力:**
```
============================================================
Google Cloud Text-to-Speech API 技術検証
============================================================
✅ 認証情報: /path/to/credentials/chat365-service-account-key.json

🔊 テキストを音声に変換中...
テキスト: こんにちは。これは、Google Cloud Text-to-Speech API...

✅ 音声ファイルを生成しました: tests/output_ja.mp3
ファイルサイズ: 12345 bytes

============================================================
複数音声タイプのテスト
============================================================
✅ NEUTRAL: tests/output_ja_neutral.mp3
✅ FEMALE: tests/output_ja_female.mp3
✅ MALE: tests/output_ja_male.mp3

============================================================
✅ 技術検証: 成功
============================================================

📢 生成された音声ファイルを再生して確認してください
   macOSの場合: open tests/output_ja.mp3
```

音声ファイルを再生:

```bash
# macOS
open tests/output_ja.mp3

# Linux (mpg123がインストールされている場合)
mpg123 tests/output_ja.mp3

# Windows
start tests/output_ja.mp3
```

---

## 5. バックエンドサーバーの起動

### 5.1 データベースの初期化

```bash
cd src/backend
python init_db.py
```

### 5.2 サーバーの起動

```bash
python app.py
```

**期待される出力:**
```
 * Running on http://127.0.0.1:5001
```

### 5.3 動作確認

ブラウザで http://localhost:5001 にアクセスし、フロントエンドが表示されることを確認。

---

## 6. トラブルシューティング

### 問題: `ModuleNotFoundError: No module named 'google'`

**解決策:**
```bash
pip install google-cloud-speech google-cloud-texttospeech
```

### 問題: `google.auth.exceptions.DefaultCredentialsError`

**解決策:**
環境変数が正しく設定されていません。

```bash
# 環境変数を確認
echo $GOOGLE_APPLICATION_CREDENTIALS

# 設定されていない場合
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

### 問題: `403 Forbidden` エラー

**原因:** APIが有効化されていない、または請求先アカウントが未設定

**解決策:**
1. Google Cloud Consoleで該当APIが有効化されているか確認
2. プロジェクトに請求先アカウントが紐付いているか確認

### 問題: 音声ファイルが再生されない（Linux）

**解決策:**
```bash
# PulseAudioまたはALSAが必要
sudo apt-get install pulseaudio alsa-utils

# pygameの音声再生に必要
sudo apt-get install python3-pygame
```

### 問題: 音声認識の精度が低い

**解決策:**
- 録音形式を確認: WAV, 16000Hz, モノラル
- 背景ノイズを減らす
- マイクの音量を調整

---

## 7. 次のステップ

✅ セットアップが完了したら、次は開発計画に従って実装を進めます:

1. **Phase 1**: コア技術検証（完了）
2. **Phase 2**: バックエンド基盤構築
3. **Phase 3**: スケジューリング機能実装
4. **Phase 4**: フロントエンド実装
5. **Phase 5**: 統合テスト
6. **Phase 6**: ドキュメント整備・デプロイ

詳細は `docs/development_plan.md` を参照してください。

---

## 8. 参考資料

- [Google Cloud Speech-to-Text ドキュメント](https://cloud.google.com/speech-to-text/docs)
- [Google Cloud Text-to-Speech ドキュメント](https://cloud.google.com/text-to-speech/docs)
- [Python クイックスタート（Speech-to-Text）](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries)
- [Python クイックスタート（Text-to-Speech）](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries)

---

**問題が解決しない場合:**
- GitHub Issuesで報告
- `docs/development_plan.md`のトラブルシューティングセクションを参照
