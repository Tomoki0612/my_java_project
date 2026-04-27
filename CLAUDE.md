# LeetCode Practice

## 毎日の流れ

```bash
python3 scripts/today.py          # 今日のタスク確認（冒頭に「次のアクション」を表示）
python3 scripts/next_action.py    # 次にやるべき1コマンドだけを1行で表示
```

### 新問題の日
```bash
python3 scripts/new_problem.py <番号> --ja   # 問題追加（日本語翻訳付き）
# ... 解く → LeetCode で Submit → Accepted を確認 ...
python3 scripts/done.py <番号>               # 長期復習サイクルへ
python3 scripts/done.py <番号> --helped      # ヒントが必要だった → 翌日復習
```

### 復習の日
```bash
python3 scripts/review.py <番号>   # 前回答えをバックアップ → Solution.java をリセット
# ... 解く → LeetCode で Submit → Accepted を確認 ...
python3 scripts/done.py <番号>     # 次のステージへ
python3 scripts/done.py <番号> --helped   # また詰まった → ステージリセット
```

`done.py` は **LeetCode で Accepted を取った後に実行する**。
ローカルテストはサンプルケースしか抽出していないため、タイポ検知用の参考情報扱い
（失敗してもブロックしない、警告のみ）。`--no-test` でローカル実行自体を省略可。

## 間隔反復 (Spaced Repetition)

`done.py` で正解するたびにステージが上がり、復習間隔が伸びる：

| stage | 次回までの日数 |
|-------|----------------|
| 0     | 1日            |
| 1     | 3日            |
| 2     | 7日            |
| 3     | 21日           |
| 4     | 60日           |
| 5     | 180日 (mastered) |

- `--helped` を付けると stage 0 にリセット（翌日また復習）
- 最終ステージに到達 = `mastered`、ただし 180日後に長期復習として再度出題される
- 新規問題を初回自力で正解した場合は一気に最終ステージへ昇格

## 履歴 (history)

各エントリに `history: [{date, result, stage}]` を保存。`done.py` 実行ごとに自動追記され、
日付ベースの分析（streak、ペース計測、復習成功率など）の素材になる。

## CI

`.github/workflows/test.yml` が `mastered` ステータスのテストだけを GitHub Actions で実行し、
回帰検出する。`scripts/list_mastered_tests.py` がテストクラスを動的に列挙する。

## トピックタグと弱点分析

- 新規追加時に LeetCode の `topicTags` を `progress.json` に保存
- `today.py` がリトライ累計の多いトピックを「弱点トピック」として表示
- 既存エントリへの後付けは一回限り `python3 scripts/backfill_tags.py` を実行

## フォルダ構成

```
src/
  main/java/leetcode/
    common/            # ListNode, TreeNode など共通クラス
    p0001_two_sum/
      Solution.java    # 解答
    progress.json      # 問題ステータス管理
  test/java/leetcode/
    p0001_two_sum/
      SolutionTest.java  # JUnit 5 テスト（サンプルケース自動生成）
backups/               # 復習時の前回答えバックアップ（gitignore済み）
scripts/
  progress_lib.py      # ステージ遷移・スキーマ管理の共通ロジック
  today.py / new_problem.py / done.py / review.py / import_mastered.py / backfill_tags.py
```

## ステータス遷移

```
new_problem.py → [in_progress]
                     │
                     ├── done.py          → [mastered] (stage 5, 180日後に長期復習)
                     └── done.py --helped → [review] (stage 0, 翌日復習)
                                              │
                                              ├── done.py          → stage++ (1→3→7→21→60→180)
                                              └── done.py --helped → stage 0 リセット
```
