#!/usr/bin/env python3
"""
復習モード: 前回の解答をバックアップして Solution.java をリセットする

Usage:
  python3 scripts/review.py <問題番号>
"""
import sys
import os
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import (
    PROJECT_ROOT, SRC_ROOT,
    load_progress, save_progress, find_key,
)
from new_problem import fetch_problem, build_solution


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/review.py <問題番号>")
        sys.exit(1)

    number = int(sys.argv[1])
    progress, dirty = load_progress()
    key = find_key(progress, number)

    if not key:
        print(f"問題 #{number} は未登録です。")
        sys.exit(1)

    entry = progress[key]
    if entry["status"] not in ("review", "mastered"):
        print(f"#{number} {entry['title']} は復習対象ではありません (status: {entry['status']})")
        sys.exit(1)

    if dirty:
        save_progress(progress)

    dir_path = os.path.join(SRC_ROOT, key)
    solution_path = os.path.join(dir_path, "Solution.java")

    if not os.path.exists(solution_path):
        print(f"Solution.java が見つかりません: {solution_path}")
        sys.exit(1)

    from datetime import date
    backup_dir = os.path.join(PROJECT_ROOT, "backups", key)
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, f"{date.today().isoformat()}.java")
    shutil.copy2(solution_path, backup_path)
    print(f"バックアップ: backups/{key}/{date.today().isoformat()}.java")

    slug = key[6:].replace("_", "-")
    print(f"問題情報を取得中: {slug} ...")
    problem = fetch_problem(slug)
    if not problem:
        print(f"問題情報の取得に失敗しました: {slug}")
        sys.exit(1)

    _, template = build_solution(problem, translate=False)
    with open(solution_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"リセット完了: #{number} {entry['title']} [{entry['difficulty']}]")
    print(f"  解けたら     → python3 scripts/done.py {number}")
    print(f"  詰まったら   → python3 scripts/done.py {number} --helped")


if __name__ == "__main__":
    main()
