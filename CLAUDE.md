# LeetCode Practice

## 毎日の流れ

```bash
python3 scripts/today.py          # 今日のタスク確認（まずこれ）
```

### 新問題の日
```bash
python3 scripts/new_problem.py <番号> --ja   # 問題追加（日本語翻訳付き）
# ... 解く ...
python3 scripts/done.py <番号>               # 自力で解けた → mastered
python3 scripts/done.py <番号> --helped      # ヒントが必要だった → 翌日復習
```

### 復習の日
```bash
python3 scripts/review.py <番号>   # 前回答えをバックアップ → Solution.java をリセット
# ... 解く ...
python3 scripts/done.py <番号>     # 自力で解けた → mastered
python3 scripts/done.py <番号> --helped   # また詰まった → 翌日も復習
```

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
scripts/               # 管理スクリプト
```

## ステータス遷移

```
new_problem.py → [in_progress] → done.py --helped → [review] → done.py → [mastered]
                                                                  ↓
                                                             done.py --helped → [review]（翌日また復習）
```
