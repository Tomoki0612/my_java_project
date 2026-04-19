#!/usr/bin/env python3
"""今日やることを表示する"""
import json
import os
import subprocess
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRESS_FILE = os.path.join(PROJECT_ROOT, "src", "main", "java", "leetcode", "progress.json")


def git_pull():
    result = subprocess.run(
        ["git", "pull", "--rebase"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        msg = result.stdout.strip()
        print(f"[git] {msg if msg else 'Already up to date.'}")
    else:
        print(f"[git] pull 失敗: {result.stderr.strip()}")


def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        return json.load(f)


def main():
    git_pull()
    progress = load_progress()
    today = date.today().isoformat()

    reviews  = [(k, v) for k, v in progress.items() if v["status"] == "review" and v.get("next_review", "") <= today]
    in_prog  = [(k, v) for k, v in progress.items() if v["status"] == "in_progress"]
    mastered = [v for v in progress.values() if v["status"] == "mastered"]

    print(f"=== 今日のタスク ({today}) ===\n")

    if reviews:
        print("復習")
        for k, v in reviews:
            num = int(k[1:5])
            retries = v.get("retries", 0)
            retry_str = f"  (今日で{retries + 1}回目の挑戦)" if retries else ""
            print(f"  #{num} {v['title']} [{v['difficulty']}]{retry_str}")
            print(f"       自力で解けた → python3 scripts/done.py {num}")
            print(f"       また詰まった → python3 scripts/done.py {num} --helped")
        print()

    if in_prog:
        print("取り組み中")
        for k, v in in_prog:
            num = int(k[1:5])
            print(f"  #{num} {v['title']} [{v['difficulty']}]")
            print(f"       自力で解けた → python3 scripts/done.py {num}")
            print(f"       ヒントが必要 → python3 scripts/done.py {num} --helped")
        print()

    if not reviews and not in_prog:
        print("新しい問題を追加しましょう")
        print("  python3 scripts/new_problem.py <番号> --ja\n")

    total = len(progress)
    review_count = len([v for v in progress.values() if v["status"] == "review"])
    print(f"--- 進捗: 習得済み {len(mastered)}問 / 合計 {total}問", end="")
    if review_count:
        print(f" / 復習待ち {review_count}問", end="")
    print()


if __name__ == "__main__":
    main()
