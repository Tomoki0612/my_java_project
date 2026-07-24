#!/usr/bin/env python3
"""学習環境の前提条件を読み取り専用で診断する。"""
import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request

from progress_lib import PROJECT_ROOT


def run(command):
    return subprocess.run(command, cwd=PROJECT_ROOT, capture_output=True, text=True)


def java_check():
    try:
        result = run(["java", "-version"])
    except FileNotFoundError:
        return False, "Java なし", "Java 17以上をインストールしてください"
    output = (result.stderr or result.stdout).strip()
    match = re.search(r'version "(\d+)', output)
    major = int(match.group(1)) if match else None
    return bool(major and major >= 17), f"Java {major or '?'}", "Java 17以上をJAVA_HOME/PATHで有効にしてください"


def command_check(command, label):
    try:
        result = run(command)
    except FileNotFoundError:
        return False, f"{label} なし", f"{label}をインストールしてください"
    first = (result.stdout or result.stderr).splitlines()
    return result.returncode == 0, first[0] if first else label, "コマンド実行に失敗しました"


def network_check():
    try:
        request = urllib.request.Request(
            "https://leetcode.com/graphql",
            headers={"User-Agent": "Mozilla/5.0", "Referer": "https://leetcode.com"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status < 500, f"HTTP {response.status}", "LeetCodeへ接続できません"
    except Exception as exc:
        if isinstance(exc, urllib.error.HTTPError) and exc.code < 500:
            return True, f"HTTP {exc.code}（到達可能）", ""
        return False, str(exc), "ネットワークまたはLeetCodeの状態を確認してください"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Java学習環境を診断する")
    parser.add_argument("--offline", action="store_true", help="LeetCode接続確認を省略")
    args = parser.parse_args(argv)

    checks = [
        ("Java", java_check()),
        ("Maven", command_check(["mvn", "-version"], "Maven")),
        ("Git", command_check(["git", "rev-parse", "--is-inside-work-tree"], "Git")),
    ]
    if not args.offline:
        checks.append(("LeetCode", network_check()))

    failed = False
    for label, (ok, detail, advice) in checks:
        print(f"[{'OK' if ok else 'NG'}] {label}: {detail}")
        if not ok:
            failed = True
            print(f"     → {advice}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
