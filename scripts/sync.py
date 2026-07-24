#!/usr/bin/env python3
"""学習データと解答だけを確認付きでcommit/pull/pushする。"""
import argparse
import subprocess
import sys

from progress_lib import PROJECT_ROOT

LEARNING_PATHS = (
    "src/main/java/leetcode",
    "src/test/java/leetcode",
    "scripts",
    "README.md",
    "CLAUDE.md",
    "Makefile",
    "pom.xml",
    ".github/workflows/test.yml",
)


def run(command, check=False, capture=False):
    return subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=check,
        text=True,
        capture_output=capture,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="学習内容を明示的にGit同期する")
    parser.add_argument("-m", "--message", default="progress: update learning record")
    parser.add_argument("--yes", action="store_true", help="確認を省略")
    args = parser.parse_args(argv)

    staged = run(["git", "diff", "--cached", "--name-only"], capture=True).stdout.strip()
    if staged:
        print("既にstage済みの変更があります。混在を避けるため中止します:")
        print(staged)
        return 1

    run(["git", "add", "--", *LEARNING_PATHS], check=True)
    files = run(["git", "diff", "--cached", "--name-only"], capture=True).stdout.strip()
    if not files:
        print("同期対象の学習変更はありません。")
        return 0

    print("同期対象:")
    print(files)
    if not args.yes and input("commitしてpushしますか? [y/N] ").strip().lower() != "y":
        run(["git", "restore", "--staged", "--", *LEARNING_PATHS], check=True)
        print("中止しました（ファイル変更は保持されています）")
        return 1

    run(["git", "commit", "-m", args.message], check=True)
    run(["git", "pull", "--rebase"], check=True)
    run(["git", "push"], check=True)
    print("同期完了")
    return 0


if __name__ == "__main__":
    sys.exit(main())
