#!/usr/bin/env python3
"""
既存の progress.json エントリに topic_tags を後付けする一回限りのスクリプト。

Usage:
  python3 scripts/backfill_tags.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import load_progress, save_progress
from new_problem import fetch_problem


def main():
    progress, dirty = load_progress()

    targets = [k for k, v in progress.items() if not v.get("topic_tags")]
    if not targets:
        print("全エントリにタグが既に設定されています")
        if dirty:
            save_progress(progress)
            print("(マイグレーションだけ保存しました)")
        return

    print(f"{len(targets)}問のタグを取得します...")
    failed = []
    for key in targets:
        slug = key[6:].replace("_", "-")
        try:
            problem = fetch_problem(slug)
            tags = [t["name"] for t in (problem.get("topicTags") or [])]
            progress[key]["topic_tags"] = tags
            print(f"  {key}: {tags}")
        except Exception as e:
            print(f"  {key}: 取得失敗 ({e})")
            failed.append(key)
        time.sleep(0.3)  # LeetCode API への配慮

    save_progress(progress)
    print(f"\n完了: {len(targets) - len(failed)}/{len(targets)} 件にタグを設定")
    if failed:
        print(f"失敗: {failed}")


if __name__ == "__main__":
    main()
