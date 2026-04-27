#!/usr/bin/env python3
"""
解いた結果を記録する。

LeetCode で Accepted が出たことを確認してから実行すること。
ローカルテストはサンプルケースのみなので「タイポ検知」用の参考情報扱い。

Usage:
  python3 scripts/done.py <問題番号>              # LeetCode Accepted を記録 → ステージ昇格
  python3 scripts/done.py <問題番号> --helped     # ヒントあり → ステージリセット
  python3 scripts/done.py <問題番号> --no-test    # ローカルテスト実行もスキップ
"""
import sys
import os
import shutil
import subprocess
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import (
    PROJECT_ROOT, SRC_ROOT, PROGRESS_FILE,
    load_progress, save_progress, find_key, apply_transition,
    INTERVALS_DAYS, MAX_STAGE,
)
from new_problem import fetch_problem, build_solution


def run_tests(pkg_dir):
    """指定パッケージのテストを実行。

    Returns:
      (None, msg) : テストファイルが無いのでスキップ
      (True, out) : 成功
      (False, out): 失敗
    """
    test_file = os.path.join(
        PROJECT_ROOT, "src", "test", "java", "leetcode", pkg_dir, "SolutionTest.java"
    )
    if not os.path.exists(test_file):
        return None, "テストファイルが存在しません"

    cls = f"leetcode.{pkg_dir}.SolutionTest"
    result = subprocess.run(
        ["mvn", "-q", "test", f"-Dtest={cls}"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    out = (result.stdout + result.stderr).strip()
    return result.returncode == 0, out


def git_push(message, key):
    """progress.json と該当 Solution.java をまとめて commit/push する。"""
    sol_path = os.path.join(SRC_ROOT, key, "Solution.java")
    files = [PROGRESS_FILE]
    if os.path.exists(sol_path):
        files.append(sol_path)
    subprocess.run(["git", "add", "--"] + files, cwd=PROJECT_ROOT, check=True)
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=PROJECT_ROOT)
    if result.returncode == 0:
        return
    subprocess.run(["git", "commit", "-m", message], cwd=PROJECT_ROOT, check=True)
    subprocess.run(["git", "push"], cwd=PROJECT_ROOT, check=True)
    print(f"  [git] push 完了")


def reset_solution(key):
    dir_path = os.path.join(SRC_ROOT, key)
    solution_path = os.path.join(dir_path, "Solution.java")
    if not os.path.exists(solution_path):
        return
    today = date.today().isoformat()
    backup_dir = os.path.join(PROJECT_ROOT, "backups", key)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(solution_path, os.path.join(backup_dir, f"{today}.java"))
    print(f"  バックアップ: backups/{key}/{today}.java")

    slug = key[6:].replace("_", "-")
    problem = fetch_problem(slug)
    if not problem:
        print(f"  ※ 問題情報の取得に失敗したためリセットをスキップしました")
        return
    _, template = build_solution(problem, translate=False)
    with open(solution_path, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"  Solution.java をリセットしました")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/done.py <問題番号> [--helped] [--no-test]")
        sys.exit(1)

    number = int(sys.argv[1])
    helped = "--helped" in sys.argv
    skip_test = "--no-test" in sys.argv

    progress, _ = load_progress()
    key = find_key(progress, number)
    if not key:
        print(f"問題 #{number} は未登録です。先に new_problem.py で追加してください。")
        sys.exit(1)

    entry = progress[key]
    title = entry["title"]
    difficulty = entry["difficulty"]

    # ローカルテストはタイポ検知用の参考情報。失敗してもブロックしない。
    # 真の合否は LeetCode の Submit で確認する前提。
    if not helped and not skip_test:
        try:
            input("  Solution.java を保存しましたか? [Enter で続行 / Ctrl+C で中止] ")
        except KeyboardInterrupt:
            print("\n  中止しました")
            sys.exit(1)
        print(f"  ローカルテスト: leetcode.{key}.SolutionTest ...")
        ok, out = run_tests(key)
        if ok is None:
            print(f"  [skip] {out}")
        elif not ok:
            print("  [warn] ローカルテスト失敗。LeetCode で本当に Accepted が出たか再確認推奨。")
            print("  ----- mvn output -----")
            print(out)
            print("  ----------------------")
        else:
            print("  ローカルテスト OK")

    apply_transition(entry, helped=helped)
    save_progress(progress)

    stage = entry["stage"]
    next_review = entry["next_review"]
    days = INTERVALS_DAYS[stage]

    if helped:
        retries = entry["retries"]
        print(f"[復習リセット] #{number} {title} [{difficulty}]")
        print(f"  → {next_review} に復習 (次回で{retries + 1}回目の挑戦, stage {stage})")
        reset_solution(key)
        git_push(f"progress: #{number} {title} → review (stage {stage})", key)
    elif stage == MAX_STAGE:
        retries = entry.get("retries", 0)
        retry_str = f"  ({retries}回リトライ)" if retries else ""
        print(f"[習得！] #{number} {title} [{difficulty}]{retry_str}")
        print(f"  → 長期復習: {next_review} ({days}日後)")
        git_push(f"progress: #{number} {title} → mastered", key)
    else:
        print(f"[ステージアップ] #{number} {title} [{difficulty}] → stage {stage}")
        print(f"  → 次回復習: {next_review} ({days}日後)")
        git_push(f"progress: #{number} {title} → review (stage {stage})", key)


if __name__ == "__main__":
    main()
