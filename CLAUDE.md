# Repository Guide

利用者向けの最新手順と学習ルールは [README.md](README.md) を参照すること。

## 実装時の注意

- Java 17 / Maven / JUnit 5を使用する。
- `src/main/java/leetcode/progress.json` は既存履歴との後方互換性を保つ。
- `done.py` は評価保存後、その問題の解答と進捗だけを自動commit・pushする。
  その他の同期は `make sync` に限定する。
- LeetCode Acceptedを最終判定とし、生成JUnitはタイポ・回帰検出として扱う。
- 進捗・評価・日程計算は `scripts/progress_lib.py`、面接パターン分析は
  `scripts/interview_lib.py` に集約する。
- Pythonスクリプトのテストは `make test-scripts` で実行する。
