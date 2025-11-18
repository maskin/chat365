# Phase 1: プロジェクト準備・技術検証 - 作業記録

**作業日**: 2024-11-18  
**フェーズ**: Phase 0 → Phase 1  
**ステータス**: Phase 0完了、Phase 1準備完了  
**次回担当者への引き継ぎ文書**

---

## 📋 本日の作業サマリー

### 完了した作業

1. ✅ **プロジェクト企画・要件定義**
   - 要件定義書の作成
   - 開発計画書（8週間）の作成
   - セットアップガイドの作成

2. ✅ **リポジトリ初期化**
   - GitHubリポジトリ作成: `maskin/chat365`
   - .gitignoreの設定
   - 初回コミット＆プッシュ

3. ✅ **開発環境セットアップ**
   - Python仮想環境の構築
   - Google Cloud APIライブラリのインストール
   - 技術検証スクリプトの作成

### 未完了の作業（次回実施）

- ⏭️ Google Cloudプロジェクトのセットアップ
- ⏭️ Speech-to-Text API / Text-to-Speech APIの動作検証
- ⏭️ スケジューラー（APScheduler）の動作検証

---

## 📁 作成したファイル一覧

### ドキュメント

| ファイル名 | 内容 | 重要度 |
|-----------|------|--------|
| `docs/requirements.md` | 機能要件・非機能要件・API仕様 | ⭐⭐⭐ |
| `docs/development_plan.md` | 8週間の開発計画・マイルストーン | ⭐⭐⭐ |
| `docs/setup_guide.md` | 環境セットアップの詳細手順 | ⭐⭐⭐ |
| `docs/db_design.md` | データベース設計（既存） | ⭐⭐ |
| `docs/tech_validation.md` | 技術検証計画（既存） | ⭐⭐ |

### テストスクリプト

| ファイル名 | 内容 | 実行状況 |
|-----------|------|---------|
| `tests/speech_test.py` | Speech-to-Text API検証スクリプト | 未実行（認証設定待ち） |
| `tests/tts_test.py` | Text-to-Speech API検証スクリプト | 未実行（認証設定待ち） |

### 設定ファイル

| ファイル名 | 内容 |
|-----------|------|
| `.gitignore` | Git除外設定（DB、認証情報、音声ファイル等） |
| `venv/` | Python仮想環境（作成済み、.gitignoreで除外） |

### 既存ファイル（コミット済み）

- `src/backend/app.py` - Flaskアプリケーション（基本API実装済み）
- `src/backend/database.py` - SQLAlchemyモデル定義
- `src/backend/init_db.py` - データベース初期化スクリプト
- `src/backend/requirements.txt` - Python依存パッケージ
- `src/frontend/index.html` - フロントエンドHTML
- `src/frontend/script.js` - フロントエンドJavaScript
- `src/frontend/style.css` - フロントエンドCSS

---

## 🔧 環境情報

### システム環境

- **OS**: macOS (Darwin)
- **Python**: 3.12.5 (pyenv管理)
- **Git**: インストール済み
- **GitHub CLI**: `gh` コマンド利用可能

### インストール済みPythonパッケージ

```
google-cloud-speech      # Speech-to-Text API用
google-cloud-texttospeech # Text-to-Speech API用
apscheduler              # スケジューリング用
pygame                   # 音声再生用
pydub                    # 音声処理用
Flask                    # Webフレームワーク
SQLAlchemy               # ORM
```

### GitHubリポジトリ

- **URL**: https://github.com/maskin/chat365
- **ブランチ**: main
- **最新コミット**: `718dcba` - "Phase 1準備: 技術検証スクリプトとセットアップガイドを追加"
- **リモート**: origin (HTTPS)

---

## 🎯 次回作業: Phase 1 技術検証

### Phase 1の目的

Google Cloud APIとスケジューラーの動作を検証し、技術的リスクを早期に特定する。

### 実施タスク（推定3-5日）

#### 1. Google Cloudプロジェクトのセットアップ（半日）

**手順**:

1. **プロジェクト作成**
   ```
   - Google Cloud Consoleにアクセス: https://console.cloud.google.com/
   - 新しいプロジェクトを作成
   - プロジェクト名: chat365-broadcast（推奨）
   ```

2. **APIの有効化**
   ```
   APIとサービス → ライブラリ
   ├─ Cloud Speech-to-Text API → 有効化
   └─ Cloud Text-to-Speech API → 有効化
   ```

3. **サービスアカウント作成**
   ```
   IAMと管理 → サービスアカウント → 作成
   - 名前: chat365-service-account
   - ロール:
     ├─ Cloud Speech 管理者
     └─ Cloud Text-to-Speech 管理者
   ```

4. **認証キーのダウンロード**
   ```
   サービスアカウント → キー → 新しい鍵を作成
   - タイプ: JSON
   - ダウンロードされたファイル名例: chat365-xxxx.json
   ```

5. **認証情報の配置**
   ```bash
   cd /Users/maskin/Library/CloudStorage/Dropbox/0.github/chat365
   mkdir -p credentials
   mv ~/Downloads/chat365-xxxx.json credentials/
   ```

6. **環境変数の設定**
   ```bash
   # ~/.zshrc または ~/.bashrc に追加
   export GOOGLE_APPLICATION_CREDENTIALS="/Users/maskin/Library/CloudStorage/Dropbox/0.github/chat365/credentials/chat365-xxxx.json"
   
   # 設定を反映
   source ~/.zshrc
   ```

7. **確認**
   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   ls -l $GOOGLE_APPLICATION_CREDENTIALS
   ```

#### 2. Speech-to-Text API動作検証（1日）

**準備**:

テスト用音声ファイルの作成が必要です。

```bash
# macOSの場合: QuickTime Playerで録音
# 1. アプリケーション → QuickTime Player → ファイル → 新規オーディオ収録
# 2. 録音ボタンをクリックして以下を読み上げる:
#    「こんにちは。これは音声認識のテストです。本日は晴天なり。」
# 3. 停止して保存
#    - 形式: WAVに変換（必要に応じてAudacityなどで変換）
#    - サンプルレート: 16000Hz
#    - チャンネル: モノラル
# 4. 保存先: tests/test_audio_ja.wav
```

**実行**:

```bash
cd /Users/maskin/Library/CloudStorage/Dropbox/0.github/chat365
source venv/bin/activate
python tests/speech_test.py
```

**期待される結果**:

```
✅ 認証情報が確認される
✅ 音声ファイルが認識される
✅ 日本語テキストが出力される
✅ 信頼度が80%以上
```

**判定基準**:

- ✅ 成功: 上記すべてが満たされる → Phase 1完了へ
- ❌ 失敗: APIエラー、精度不足 → 代替手段検討

#### 3. Text-to-Speech API動作検証（1日）

**実行**:

```bash
python tests/tts_test.py
```

**期待される結果**:

```
✅ 認証情報が確認される
✅ 音声ファイルが生成される（tests/output_ja.mp3）
✅ 複数音声タイプ（NEUTRAL, FEMALE, MALE）が生成される
```

**確認事項**:

```bash
# 生成された音声を再生して確認
open tests/output_ja.mp3

# 確認ポイント:
# - 日本語として自然か
# - イントネーションは適切か
# - 聞き取りやすいか
```

**判定基準**:

- ✅ 成功: 自然で聞き取りやすい音声 → Phase 1完了へ
- ⚠️ 要改善: やや不自然だが使用可能 → パラメータ調整
- ❌ 失敗: 使用不可レベル → 代替API検討

#### 4. スケジューラー動作検証（1日）

**検証スクリプトの作成**:

```python
# tests/scheduler_test.py を新規作成
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import time

def test_job():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ジョブ実行！")

scheduler = BackgroundScheduler()

# 5秒後に実行
run_time = datetime.now() + timedelta(seconds=5)
scheduler.add_job(test_job, 'date', run_date=run_time)

scheduler.start()
print(f"スケジューラー起動。{run_time.strftime('%H:%M:%S')}に実行予定")

time.sleep(10)
scheduler.shutdown()
```

**実行**:

```bash
python tests/scheduler_test.py
```

**期待される結果**:

```
✅ 指定時刻±5秒以内でジョブが実行される
✅ 複数ジョブの並行実行が可能
```

#### 5. 検証結果のドキュメント化（半日）

**作成するファイル**:

`docs/tech_validation_result.md`

**記載内容**:

```markdown
# 技術検証結果レポート

## 実施日
2024-11-XX

## 検証結果サマリー
- Speech-to-Text API: ✅ 合格 / ❌ 不合格
- Text-to-Speech API: ✅ 合格 / ❌ 不合格
- APScheduler: ✅ 合格 / ❌ 不合格

## 詳細

### Speech-to-Text
- 認識精度: XX%
- 処理時間: XX秒（10秒音声）
- 課題: （あれば記載）

### Text-to-Speech
- 音声品質: 自然 / やや不自然 / 不自然
- 生成時間: XX秒（100文字）
- 推奨音声タイプ: NEUTRAL / FEMALE / MALE

### スケジューラー
- 実行精度: ±XX秒
- 並行実行: 問題なし / 問題あり

## 結論
Phase 1の技術検証は（合格 / 条件付き合格 / 不合格）

## 次のアクション
- Phase 2に進む / パラメータ調整 / 代替技術検討
```

---

## ⚠️ 注意事項・引き継ぎポイント

### 重要な制約事項

1. **Google Cloud API無料枠**
   - Speech-to-Text: 月間60分まで無料
   - Text-to-Speech: 月間400万文字まで無料
   - 超過分は従量課金（要注意）

2. **認証情報の管理**
   ```
   ⚠️ credentials/*.json は絶対にGitにコミットしない！
   → .gitignoreで除外済み
   ```

3. **音声ファイル形式**
   - Speech-to-Text入力: WAV, 16000Hz, モノラル推奨
   - Text-to-Speech出力: MP3形式

### トラブルシューティング

#### 問題1: `google.auth.exceptions.DefaultCredentialsError`

**原因**: 環境変数が設定されていない

**解決策**:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/key.json"
source ~/.zshrc
```

#### 問題2: `ModuleNotFoundError: No module named 'google'`

**原因**: ライブラリがインストールされていない

**解決策**:
```bash
source venv/bin/activate
pip install google-cloud-speech google-cloud-texttospeech
```

#### 問題3: 音声ファイルが認識されない

**原因**: ファイル形式が不適切

**解決策**:
```bash
# Audacityで変換
# - サンプルレート: 16000Hz
# - チャンネル: モノラル
# - 形式: WAV (PCM)
```

---

## 📊 進捗状況

### Phase 0: プロジェクト準備（完了 ✅）

- [x] プロジェクト構成確認
- [x] ドキュメントレビュー
- [x] 要件定義書作成
- [x] 開発計画書作成
- [x] Gitリポジトリ初期化
- [x] .gitignore設定
- [x] Python仮想環境構築
- [x] 依存パッケージインストール
- [x] 技術検証スクリプト作成
- [x] GitHubリポジトリ作成・プッシュ

### Phase 1: 技術検証（準備完了、実施待ち 🔄）

- [ ] Google Cloudプロジェクト作成
- [ ] Speech-to-Text API有効化
- [ ] Text-to-Speech API有効化
- [ ] サービスアカウント作成
- [ ] 認証キーダウンロード・配置
- [ ] 環境変数設定
- [ ] テスト音声ファイル準備
- [ ] Speech-to-Text動作検証
- [ ] Text-to-Speech動作検証
- [ ] APScheduler動作検証
- [ ] 検証結果レポート作成

---

## 🔗 参考リソース

### ドキュメント

- [README.md](../README.md) - プロジェクト概要
- [HANDOVER.md](../HANDOVER.md) - 引き継ぎ情報
- [requirements.md](./requirements.md) - 要件定義
- [development_plan.md](./development_plan.md) - 開発計画
- [setup_guide.md](./setup_guide.md) - セットアップ手順

### 外部リンク

- [Google Cloud Console](https://console.cloud.google.com/)
- [Speech-to-Text ドキュメント](https://cloud.google.com/speech-to-text/docs)
- [Text-to-Speech ドキュメント](https://cloud.google.com/text-to-speech/docs)
- [APScheduler ドキュメント](https://apscheduler.readthedocs.io/)

### GitHubリポジトリ

- [maskin/chat365](https://github.com/maskin/chat365)

---

## 📝 作業ログ

### 2024-11-18 (本日の作業)

**時刻**: 02:00 - 02:45 (JST換算: 11:00 - 11:45)

**実施者**: GitHub Copilot CLI + maskin

**作業内容**:

1. プロジェクト全体の分析・理解
   - 既存ドキュメント（README, HANDOVER, db_design, tech_validation）のレビュー
   - 現状の実装状況確認
   - 未実装機能の洗い出し

2. 要件定義書の作成（`docs/requirements.md`）
   - 機能要件: 20以上の要件を詳細化
   - 非機能要件: 性能、可用性、セキュリティ等
   - API仕様: 6つのエンドポイント定義
   - データ要件、受け入れ基準、リスク管理

3. 開発計画書の作成（`docs/development_plan.md`）
   - 8週間のフェーズ分割（Phase 0-6）
   - 各週の詳細タスクブレークダウン
   - マイルストーン定義
   - リスク管理と対策
   - 品質管理基準

4. Gitリポジトリの初期化
   - .gitignore作成（Python、DB、認証情報を除外）
   - 初回コミット
   - GitHubリポジトリ作成（maskin/chat365）
   - リモートプッシュ（HTTPS経由）

5. 開発環境のセットアップ
   - Python仮想環境作成（venv/）
   - Google Cloud APIライブラリインストール
     - google-cloud-speech
     - google-cloud-texttospeech
   - その他依存パッケージインストール
     - apscheduler, pygame, pydub

6. 技術検証スクリプトの作成
   - `tests/speech_test.py`: Speech-to-Text API検証
   - `tests/tts_test.py`: Text-to-Speech API検証
   - 認証確認、エラーハンドリング実装

7. セットアップガイドの作成（`docs/setup_guide.md`）
   - Google Cloudセットアップ手順
   - ローカル環境構築手順
   - トラブルシューティング

8. GitHubへの2回目のコミット＆プッシュ
   - 技術検証スクリプト追加
   - セットアップガイド追加

**成果物**:
- 3つの新規ドキュメント（計2,400行以上）
- 2つのテストスクリプト
- 動作確認済みの開発環境
- GitHubリポジトリ（2コミット）

**次回への申し送り**:

✅ **すぐ始められる状態になっています！**

次回作業開始時は以下の手順で進めてください:

1. `docs/setup_guide.md` を開く
2. 「2. Google Cloud プロジェクトのセットアップ」を実施
3. 認証情報を設定後、検証スクリプトを実行
4. 結果を `docs/tech_validation_result.md` に記録

**推定所要時間**: 3-4時間（APIセットアップ含む）

---

## ✅ チェックリスト: 次回作業開始前

次回作業を開始する前に、以下を確認してください:

- [ ] Gitリポジトリが最新状態か確認
  ```bash
  cd /Users/maskin/Library/CloudStorage/Dropbox/0.github/chat365
  git pull
  ```

- [ ] Python仮想環境を有効化
  ```bash
  source venv/bin/activate
  ```

- [ ] 環境変数が設定されているか確認
  ```bash
  echo $GOOGLE_APPLICATION_CREDENTIALS
  ```

- [ ] `docs/setup_guide.md` を熟読

- [ ] Google Cloudアカウントにログイン可能か確認

---

## 🎯 Phase 1完了の判定基準

Phase 1を完了とするための基準:

1. ✅ Speech-to-Text APIが正常動作（認識精度80%以上）
2. ✅ Text-to-Speech APIが正常動作（自然な音声生成）
3. ✅ APSchedulerが正常動作（±5秒以内の精度）
4. ✅ 検証結果レポートが作成されている

**全て満たした場合** → Phase 2（バックエンド基盤構築）へ進む

**1つでも不合格の場合** → 代替手段の検討、またはパラメータ調整

---

**文書管理情報**
- 作成日: 2024-11-18
- 作成者: maskin
- バージョン: 1.0
- 次回更新: Phase 1完了時

**この文書の更新方法**:
Phase 1が完了したら、「Phase 1完了」セクションを追加し、Phase 2の進捗を記録してください。
