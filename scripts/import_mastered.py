#!/usr/bin/env python3
"""
過去に解いた問題をまとめて mastered として登録する
（Solution.java は作らず progress.json のみ更新）

Usage:
  python3 scripts/import_mastered.py 1 9 13 14 ...
"""
import sys
import json
import urllib.request
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import (
    PROGRESS_FILE, INTERVALS_DAYS, MAX_STAGE,
    load_progress, save_progress,
)

GRAPHQL_URL  = "https://leetcode.com/graphql"


def fetch_problems_info(numbers):
    query = """
    query($limit: Int!, $skip: Int!) {
        questionList(categorySlug: "" limit: $limit skip: $skip filters: {}) {
            data {
                questionFrontendId
                title
                titleSlug
                difficulty
                topicTags {
                    name
                }
            }
        }
    }
    """
    result_map = {}
    max_num = max(numbers) + 1
    skip, page_size = 0, 100
    while skip < max_num:
        payload = json.dumps({"query": query, "variables": {"limit": page_size, "skip": skip}}).encode()
        req = urllib.request.Request(
            GRAPHQL_URL,
            data=payload,
            headers={"Content-Type": "application/json", "Referer": "https://leetcode.com", "User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        questions = data["data"]["questionList"]["data"]
        if not questions:
            break
        for q in questions:
            result_map[int(q["questionFrontendId"])] = q
        skip += page_size
    return result_map


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/import_mastered.py <番号1> <番号2> ...")
        sys.exit(1)

    numbers = [int(n) for n in sys.argv[1:]]
    today   = date.today()
    today_iso = today.isoformat()
    long_term_review = (today + timedelta(days=INTERVALS_DAYS[MAX_STAGE])).isoformat()

    print(f"{len(numbers)}問の情報を取得中...")
    info_map = fetch_problems_info(numbers)

    progress, _ = load_progress()

    added = 0
    for num in sorted(numbers):
        if num not in info_map:
            print(f"  #{num} 見つかりませんでした")
            continue
        q   = info_map[num]
        key = f"p{num:04d}_{q['titleSlug'].replace('-', '_')}"
        if key in progress and progress[key]["status"] == "mastered":
            continue
        progress[key] = {
            "title":        q["title"],
            "difficulty":   q["difficulty"],
            "status":       "mastered",
            "added_date":   today_iso,
            "next_review":  long_term_review,
            "mastered_date": today_iso,
            "stage":        MAX_STAGE,
            "retries":      0,
            "topic_tags":   [t["name"] for t in (q.get("topicTags") or [])],
            "history":      [],
        }
        print(f"  [mastered] #{num} {q['title']} [{q['difficulty']}]")
        added += 1

    save_progress(progress)
    print(f"\n{added}問を登録しました")


if __name__ == "__main__":
    main()
