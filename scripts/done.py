#!/usr/bin/env python3
"""解答結果を4段階評価し、短い面接向け振り返りを記録する。"""
import argparse
import os
import shutil
import subprocess
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from new_problem import build_solution, fetch_problem
from progress_lib import (
    INTERVALS_DAYS,
    MAX_STAGE,
    PROJECT_ROOT,
    RATINGS,
    SRC_ROOT,
    apply_transition,
    find_key,
    load_progress,
    normalize_rating,
    save_progress,
    validate_complexity,
)


def run_tests(pkg_dir):
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
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def _backup_path(key):
    backup_dir = os.path.join(PROJECT_ROOT, "backups", key)
    os.makedirs(backup_dir, exist_ok=True)
    base = date.today().isoformat()
    candidate = os.path.join(backup_dir, f"{base}.java")
    suffix = 2
    while os.path.exists(candidate):
        candidate = os.path.join(backup_dir, f"{base}-{suffix}.java")
        suffix += 1
    return candidate


def reset_solution(key):
    solution_path = os.path.join(SRC_ROOT, key, "Solution.java")
    if not os.path.exists(solution_path):
        return
    backup_path = _backup_path(key)
    shutil.copy2(solution_path, backup_path)
    print(f"  バックアップ: {os.path.relpath(backup_path, PROJECT_ROOT)}")

    slug = key[6:].replace("_", "-")
    try:
        problem = fetch_problem(slug)
    except Exception as exc:
        print(f"  ※ 問題情報の取得に失敗したためリセットをスキップしました: {exc}")
        return
    if not problem:
        print("  ※ 問題情報の取得に失敗したためリセットをスキップしました")
        return
    _, template = build_solution(problem)
    with open(solution_path, "w", encoding="utf-8") as file:
        file.write(template)
    print("  Solution.java をリセットしました")


def prompt_rating():
    labels = " / ".join(f"{rating[0].upper()}={rating}" for rating in RATINGS)
    while True:
        try:
            return normalize_rating(input(f"評価 ({labels}): "))
        except ValueError as exc:
            print(f"  {exc}")


def prompt_minutes(value):
    while value is None or value <= 0:
        if value is not None:
            print("  1以上の整数で入力してください")
        try:
            value = int(input("所要時間（分）: ").strip())
        except ValueError:
            value = None
    return value


def prompt_required(label, value):
    while not (value or "").strip():
        value = input(label).strip()
        if not value:
            print("  1行で入力してください")
    return value.strip()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="解答結果と短い振り返りを記録する")
    parser.add_argument("number", type=int, help="LeetCode問題番号")
    parser.add_argument("--rating", choices=RATINGS)
    parser.add_argument("--minutes", type=int)
    parser.add_argument("--pattern")
    parser.add_argument("--complexity")
    parser.add_argument("--lesson")
    parser.add_argument("--helped", action="store_true", help="--rating again の互換指定")
    parser.add_argument("--no-test", action="store_true")
    return parser.parse_args(argv)


def collect_reflection(args):
    rating = "again" if args.helped else args.rating
    if args.helped and args.rating and args.rating != "again":
        raise ValueError("--helped と --rating は同時指定できません（againを除く）")
    rating = normalize_rating(rating) if rating else prompt_rating()
    minutes = prompt_minutes(args.minutes)
    pattern = prompt_required("解法パターンと選択理由: ", args.pattern)
    complexity = args.complexity
    while not validate_complexity(complexity):
        complexity = input("計算量（例: 時間 O(n) / 空間 O(n) — HashSetに最大n件）: ").strip()
        if not validate_complexity(complexity):
            print("  O(...) を含む1行で入力してください")
    lesson = prompt_required("詰まり原因または次回の注意点（なければ「なし」）: ", args.lesson)
    return rating, minutes, pattern, complexity, lesson


def main(argv=None):
    args = parse_args(argv)
    progress, _ = load_progress()
    key = find_key(progress, args.number)
    if not key:
        print(f"問題 #{args.number} は未登録です。先に new_problem.py で追加してください。")
        return 1
    try:
        rating, minutes, pattern, complexity, lesson = collect_reflection(args)
    except ValueError as exc:
        print(exc)
        return 1

    entry = progress[key]

    if rating != "again" and not args.no_test:
        try:
            input("  Solution.java を保存しましたか? [Enterで続行 / Ctrl+Cで中止] ")
        except KeyboardInterrupt:
            print("\n  中止しました")
            return 1
        print(f"  ローカルテスト: leetcode.{key}.SolutionTest ...")
        ok, output = run_tests(key)
        if ok is None:
            print(f"  [skip] {output}")
        elif not ok:
            print("  [warn] ローカルテスト失敗。Acceptedを再確認してください。")
            print(output)
        else:
            print("  ローカルテスト OK")

    apply_transition(
        entry,
        rating=rating,
        progress=progress,
        duration_minutes=minutes,
        pattern=pattern,
        complexity=complexity,
        lesson=lesson,
    )
    save_progress(progress)

    stage = entry["stage"]
    next_review = entry["next_review"]
    title = entry["title"]
    difficulty = entry["difficulty"]
    if rating == "again":
        print(f"[Again / 復習リセット] #{args.number} {title} [{difficulty}]")
        reset_solution(key)
    elif stage == MAX_STAGE:
        print(f"[{rating.capitalize()} / 習得] #{args.number} {title} [{difficulty}]")
    else:
        print(f"[{rating.capitalize()}] #{args.number} {title} [{difficulty}] → stage {stage}")
    print(f"  → 次回復習: {next_review} ({INTERVALS_DAYS[stage]}日を基準に調整)")
    print("  ※ Git同期は必要なときに make sync を実行してください")
    return 0


if __name__ == "__main__":
    sys.exit(main())
