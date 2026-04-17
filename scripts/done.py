#!/usr/bin/env python3
"""
解いた結果を記録する

Usage:
  python3 scripts/done.py <問題番号>           # 自力で解けた → mastered
  python3 scripts/done.py <問題番号> --helped  # ヒントあり  → 翌日復習
"""
import sys
import json
import os
from datetime import date, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRESS_FILE = os.path.join(PROJECT_ROOT, "src", "main", "java", "leetcode", "progress.json")


def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_key(progress, number):
    prefix = f"p{number:04d}_"
    for key in progress:
        if key.startswith(prefix):
            return key
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/done.py <問題番号> [--helped]")
        sys.exit(1)

    number = int(sys.argv[1])
    helped = "--helped" in sys.argv
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    progress = load_progress()
    key = find_key(progress, number)

    if not key:
        print(f"問題 #{number} は未登録です。先に new_problem.py で追加してください。")
        sys.exit(1)

    entry = progress[key]
    title = entry["title"]
    difficulty = entry["difficulty"]

    if helped:
        entry["status"] = "review"
        entry["next_review"] = tomorrow
        entry["retries"] = entry.get("retries", 0) + 1
        print(f"[復習予定] #{number} {title} [{difficulty}]")
        print(f"  → {tomorrow} に復習 (次回で{entry['retries'] + 1}回目の挑戦)")
    else:
        entry["status"] = "mastered"
        entry["next_review"] = None
        entry["mastered_date"] = today
        retries = entry.get("retries", 0)
        print(f"[習得！] #{number} {title} [{difficulty}]" + (f"  ({retries}回リトライ)" if retries else ""))
        print(f"  → 明日は新しい問題へ")

    save_progress(progress)


if __name__ == "__main__":
    main()
