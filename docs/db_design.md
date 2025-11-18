# データベース設計書

## 1. 設計思想

将来的な拡張性（重複検出、ワークロード分析）と、MVP段階からのリアルタイム性（割り込み、緊急放送）を両立させることを目指す。
放送タスクの実行は、時間精度を担保するためにジョブキューシステム（例: Celery, BullMQ）の利用を前提とする。データベースは、これらのシステムが参照・更新する「状態の原本」として機能する。

## 2. テーブル定義

### `broadcasts` テーブル

放送タスクのマスターテーブル。現在スケジュールされている、あるいはこれから実行されるアクティブなタスクを管理する。

| カラム名 | データ型 | 説明 |
| :--- | :--- | :--- |
| `id` | `BIGINT` (PK) | 一意なタスクID。 |
| `uuid` | `UUID` | 外部連携用のユニバーサルユニークID。 |
| `content` | `TEXT` | 放送内容の元テキスト。 |
| `content_hash` | `VARCHAR(256)` | `content`のハッシュ値。重複検出の高速化に利用。 |
| `scheduled_at` | `TIMESTAMP WITH TIME ZONE` | 放送予定日時。タイムゾーン情報を含み、時刻の曖昧さをなくす。 |
| `duration_seconds` | `INTEGER` | 音声合成後の再生時間（秒）。ワークロード分析に使用。 |
| `priority` | `INTEGER` | 優先度。 (例: 0=通常, 1=重要, 2=緊急)。数値が高いほど優先。 |
| `task_type` | `VARCHAR(50)` | タスク種別。 ('REGULAR', 'ROUTINE', 'EMERGENCY') |
| `status` | `VARCHAR(50)` | タスクの状態。 ('SCHEDULED', 'QUEUED', 'BROADCASTING', 'COMPLETED', 'CANCELLED', 'FAILED', 'INTERRUPTED') |
| `source` | `VARCHAR(255)` | タスクの入力元情報。 (例: 'voice_input_main_console') |
| `created_at` | `TIMESTAMP WITH TIME ZONE` | レコード作成日時。 |
| `updated_at` | `TIMESTAMP WITH TIME ZONE` | レコード最終更新日時。 |
| `retry_count` | `INTEGER` | 失敗時のリトライ回数。 |
| `error_log` | `TEXT` | 実行エラー時のログ情報。 |

---

### `broadcast_log` テーブル (将来構想)

完了・失敗・キャンセル済みのタスクを保管する履歴テーブル。
`broadcasts`テーブルを常にアクティブな状態に保ち、パフォーマンスを維持するために分離する。

| カラム名 | データ型 | 説明 |
| :--- | :--- | :--- |
| `id` | `BIGINT` (PK) | ログID。 |
| `broadcast_uuid` | `UUID` | `broadcasts`テーブルのUUIDを参照。 |
| `final_status` | `VARCHAR(50)` | タスクの最終状態。('COMPLETED', 'CANCELLED', 'FAILED') |
| `started_at` | `TIMESTAMP WITH TIME ZONE` | 放送開始日時。 |
| `completed_at` | `TIMESTAMP WITH TIME ZONE` | 放送完了日時。 |
| `log_detail` | `JSONB` | 実行時の詳細なログ（実行エージェント情報など）。 |

