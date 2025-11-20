# DAY1 Plan: 音声配信デモ

## 1. 目標
本日の目標は、**音声認識 (STT)** と **音声合成 (TTS)** の基本機能が動作することをデモンストレーションすることです。
これにより、Phase 1（技術検証）の主要なマイルストーンを達成します。

## 2. 前提条件
- Google Cloud Platform (GCP) プロジェクトが作成されていること
- 以下のAPIが有効化されていること
    - Cloud Speech-to-Text API
    - Cloud Text-to-Speech API
- サービスアカウントキー（JSON）が取得済みであること

## 3. 実施手順

### 3.1 環境セットアップ
1.  **認証情報の配置**:
    - 取得したJSONキーを `credentials/` ディレクトリに配置します。
    - 環境変数 `GOOGLE_APPLICATION_CREDENTIALS` を設定します。

2.  **依存パッケージのインストール**:
    
    > [!IMPORTANT]
    > ディレクトリ名変更により仮想環境が破損しているため、再作成が必要です。

    ```bash
    # 1. 既存の仮想環境を削除して再作成
    rm -rf venv
    python3 -m venv venv

    # 2. パッケージのインストール
    ./venv/bin/pip install -r src/backend/requirements.txt
    # ./venv/bin/pip install pygame pydub  <-- pygameのビルドエラー回避のためスキップ
    # 音声再生はmacOS標準の `afplay` コマンド等を使用します
    ```
    ※ `pydub` のために `ffmpeg` が必要な場合があります（`brew install ffmpeg`）。

### 3.2 音声認識 (STT) デモ
既存のテストスクリプト `tests/speech_test.py` を使用して、音声ファイルからテキストへの変換を実演します。

- **実行コマンド**:
    ```bash
    ./venv/bin/python tests/speech_test.py
    ```
- **確認事項**:
    - コンソールに認識された日本語テキストが表示されること。
    - エラーなく終了すること。

### 3.3 音声合成 (TTS) デモ
既存のテストスクリプト `tests/tts_test.py` を使用して、テキストから音声ファイルへの変換と再生を実演します。

- **実行コマンド**:
    ```bash
    ./venv/bin/python tests/tts_test.py
    ```
- **確認事項**:
    - 音声ファイル（`tests/output_ja.mp3` 等）が生成されること。
    - 生成された音声が再生され、内容が聞き取れること。

### 3.4 (オプション) スケジューラー検証
時間があれば、`tests/verify_scheduler.py` を実行して、指定時刻にジョブが動くことを確認します。

## 4. 完了判定
- [x] STTスクリプトが正常にテキストを出力した
- [x] TTSスクリプトが正常に音声ファイルを生成した
- [x] スケジューラーがDBのタスクを処理して音声を再生した (追加要件)

---
**次のステップ**:
デモ完了後、これらの機能をバックエンドAPI (`src/backend/app.py`) に統合する作業（Phase 2）へ移行します。
