#!/usr/bin/env python3
"""今日やることを表示する"""
import os
import subprocess
import sys
from collections import Counter
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import (
    PROJECT_ROOT, load_progress, save_progress,
    INTERVALS_DAYS, MAX_STAGE,
)
from next_action import pick_next, format_one_line


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


def weak_topics(progress, limit=3):
    retries_by_topic = Counter()
    count_by_topic = Counter()
    for v in progress.values():
        for t in v.get("topic_tags") or []:
            count_by_topic[t] += 1
            retries_by_topic[t] += v.get("retries", 0) or 0
    weak = [(t, retries_by_topic[t], count_by_topic[t])
            for t in retries_by_topic if retries_by_topic[t] > 0]
    weak.sort(key=lambda x: x[1], reverse=True)
    return weak[:limit]


def main():
    git_pull()
    progress, dirty = load_progress()
    if dirty:
        save_progress(progress)
        print("[migrate] progress.json を新スキーマ (stage/next_review) に補完しました")

    today = date.today().isoformat()

    short_reviews = []
    long_reviews = []
    in_prog = []
    for k, v in progress.items():
        nr = v.get("next_review")
        status = v.get("status")
        if status == "in_progress":
            in_prog.append((k, v))
        elif nr and nr <= today:
            if status == "mastered":
                long_reviews.append((k, v))
            else:
                short_reviews.append((k, v))

    print(f"=== 今日のタスク ({today}) ===\n")
    print(format_one_line(pick_next(progress, today)))
    print()

    if short_reviews:
        print("復習")
        for k, v in short_reviews:
            num = int(k[1:5])
            retries = v.get("retries", 0) or 0
            stage = v.get("stage", 0) or 0
            retry_str = f"  (今日で{retries + 1}回目の挑戦)" if retries else ""
            print(f"  #{num} {v['title']} [{v['difficulty']}] stage {stage}{retry_str}")
            print(f"       自力で解けた → python3 scripts/done.py {num}")
            print(f"       また詰まった → python3 scripts/done.py {num} --helped")
        print()

    if long_reviews:
        print("長期復習（習得済みの再確認）")
        for k, v in long_reviews:
            num = int(k[1:5])
            mastered_date = v.get("mastered_date") or "?"
            print(f"  #{num} {v['title']} [{v['difficulty']}] 前回習得: {mastered_date}")
            print(f"       自力で解けた → python3 scripts/done.py {num}")
            print(f"       詰まった     → python3 scripts/done.py {num} --helped")
        print()

    if in_prog:
        print("取り組み中")
        for k, v in in_prog:
            num = int(k[1:5])
            print(f"  #{num} {v['title']} [{v['difficulty']}]")
            print(f"       自力で解けた → python3 scripts/done.py {num}")
            print(f"       ヒントが必要 → python3 scripts/done.py {num} --helped")
        print()

    weak = weak_topics(progress)
    if weak:
        print("弱点トピック (リトライ累計が多い順)")
        for tag, retries, n in weak:
            print(f"  {tag}: 累計 {retries} retries / 該当 {n}問")
        print()

    counts = Counter(v.get("stage") for v in progress.values())
    total = sum(counts.values())
    print(f"--- 進捗: 合計 {total}問")
    n = counts.get(None, 0)
    print(f"  取り組み中       {'█' * n} {n}")
    for s in range(MAX_STAGE + 1):
        n = counts.get(s, 0)
        days = INTERVALS_DAYS[s]
        print(f"  stage {s} ({days:>3}日) {'█' * n} {n}")


if __name__ == "__main__":
    main()
