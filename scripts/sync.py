#!/usr/bin/env python3
"""学習データと解答だけを確認付きでcommit/pull/pushする。"""
import argparse
import subprocess
import sys

if __package__:
    from .progress_lib import PROJECT_ROOT
else:
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


def sync_learning(args):
    staged = run(["git", "diff", "--cached", "--name-only"], check=True, capture=True).stdout.strip()
    if staged:
        print("既にstage済みの変更があります。混在を避けるため中止します:")
        print(staged)
        return 1

    committed = False
    try:
        run(["git", "add", "--", *LEARNING_PATHS], check=True)
        files = run(["git", "diff", "--cached", "--name-only"], check=True, capture=True).stdout.strip()
        if files:
            print("同期対象:")
            print(files)
            prompt = "commitしてpull・pushしますか? [y/N] "
        else:
            print("ファイル変更はありません。既存commitの同期を再試行します。")
            pending = run(["git", "log", "--oneline", "@{upstream}..HEAD"], check=True, capture=True)
            if pending.stdout.strip():
                print("未送信のcommit:")
                print(pending.stdout.strip())
            prompt = "pull・pushしますか? [y/N] "

        if not args.yes and input(prompt).strip().lower() != "y":
            print("中止しました（ファイル変更は保持されています）")
            return 1

        if files:
            run(["git", "commit", "-m", args.message], check=True)
        committed = True
    finally:
        if not committed:
            run(["git", "restore", "--staged", "--", *LEARNING_PATHS], check=True)

    run(["git", "pull", "--rebase"], check=True)
    run(["git", "push"], check=True)
    print("同期完了")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="学習内容を明示的にGit同期する")
    parser.add_argument("-m", "--message", default="progress: update learning record")
    parser.add_argument("--yes", action="store_true", help="確認を省略")
    args = parser.parse_args(argv)
    try:
        return sync_learning(args)
    except subprocess.CalledProcessError as exc:
        print("同期は完了していません。ファイル変更と作成済みcommitはローカルに残っています。")
        if exc.stderr:
            print(exc.stderr.strip())
        print("Gitのエラーを解消してから make sync を再実行してください。")
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\n同期を中止しました。ファイル変更と作成済みcommitは保持されています。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
