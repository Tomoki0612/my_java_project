#!/usr/bin/env python3
"""mastered ステータスかつ SolutionTest が存在する問題の FQN をカンマ区切りで出力する。

CI で `mvn test -Dtest="$(python3 scripts/list_mastered_tests.py)"` のように使う。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import PROJECT_ROOT, load_progress


def main():
    progress, _ = load_progress()
    classes = []
    for k, v in progress.items():
        if v.get("status") != "mastered":
            continue
        test_path = os.path.join(
            PROJECT_ROOT, "src", "test", "java", "leetcode", k, "SolutionTest.java"
        )
        if os.path.exists(test_path):
            classes.append(f"leetcode.{k}.SolutionTest")
    print(",".join(classes))


if __name__ == "__main__":
    main()
