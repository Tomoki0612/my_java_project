#!/usr/bin/env python3
"""今日やることを表示する"""
import os
import sys
from collections import Counter
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import (
    load_progress, save_progress,
    INTERVALS_DAYS, MAX_STAGE,
)
from next_action import pick_next, format_one_line
from interview_lib import CORE_PATTERNS, entry_patterns, readiness_summary, needs_easy, weakness_score


def weak_topics(progress, limit=3):
    weak = []
    for pattern in CORE_PATTERNS:
        count = sum(pattern in entry_patterns(entry) for entry in progress.values())
        weak.append((pattern, weakness_score(progress, pattern), count))
    weak.sort(key=lambda item: (-item[1], item[0]))
    return weak[:limit]


def find_entry_by_number(progress, number):
    prefix = f"p{number:04d}_"
    for key, entry in progress.items():
        if key.startswith(prefix):
            return key, entry
    return None, None


def build_daily_coach(progress, today_iso):
    action = pick_next(progress, today_iso)
    if not action:
        return [
            "今日の方針: 追加タスクなし",
            "理由: 期限の来た復習・未完了・弱点推薦がありません。",
        ]

    kind = action["kind"]
    number = action["number"]
    _, entry = find_entry_by_number(progress, number) if number else (None, None)

    if kind == "review" and entry:
        retries = entry.get("retries", 0) or 0
        stage = entry.get("stage", 0) or 0
        lines = [
            f"今日の方針: 復習を最優先。#{number} {entry['title']} を解き直す。",
            f"理由: next_review が {entry.get('next_review')} で、stage {stage} の定着確認日です。",
        ]
        if retries:
            lines.append(f"注意: Again記録が {retries} 回あります。実装前に解法の入口を一言で言語化する。")
        else:
            lines.append("注意: 記憶だけで進めず、制約と例外ケースを先に確認する。")
        lines.append(f"次: {action['command']}")
        return lines

    if kind == "in_progress" and entry:
        return [
            f"今日の方針: 未完了の #{number} {entry['title']} を閉じる。",
            "理由: 新規追加より、今の問題を完了または復習サイクルへ戻す方が優先です。",
            "注意: Accepted なら done、詰まったなら --rating again で翌日復習へ回す。",
            f"次: {action['command']}",
        ]

    if kind == "long_review" and entry:
        mastered_date = entry.get("mastered_date") or "?"
        return [
            f"今日の方針: 長期復習で #{number} {entry['title']} を再確認する。",
            f"理由: mastered ({mastered_date}) から時間を置いた忘却チェックです。",
            "注意: 迷った箇所があれば --rating again で stage 0 に戻して鍛え直す。",
            f"次: {action['command']}",
        ]

    if kind == "recommend_new":
        weak = weak_topics(progress, limit=1)
        lines = [
            "今日の方針: 新規問題を1問追加する。",
            "理由: 期限の来た復習と未完了問題がないため、弱点補強に進めます。",
        ]
        if weak:
            tag, retries, _ = weak[0]
            lines.append(f"注意: 最上位弱点は {tag} (score {retries})。推薦された1問だけに絞る。")
        lines.append(f"次: {action['command']}")
        return lines

    return [
        "今日の方針: 新しい問題を1問追加する。",
        "理由: 進行中タスクと期限復習がありません。",
        "注意: 追加後は LeetCode Accepted までやってから done する。",
        f"次: {action['command']}",
    ]


def print_daily_coach(progress, today_iso):
    print("日次コーチ")
    for line in build_daily_coach(progress, today_iso):
        print(f"  {line}")
    print()


def main():
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

    short_reviews.sort(key=lambda item: (item[1].get("next_review", ""), item[1].get("stage", 0)))
    long_reviews.sort(key=lambda item: item[1].get("next_review", ""))

    print(f"=== 今日のタスク ({today}) ===\n")
    print_daily_coach(progress, today)
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
            overdue = (date.today() - date.fromisoformat(v["next_review"])).days
            overdue_text = f" / {overdue}日超過" if overdue else ""
            print(f"       期限: {v['next_review']}{overdue_text} / 前回: {v.get('last_rating') or '未記録'}")
            print(f"       開始 → python3 scripts/review.py {num}")
        print()

    if long_reviews:
        print("長期復習（習得済みの再確認）")
        for k, v in long_reviews:
            num = int(k[1:5])
            mastered_date = v.get("mastered_date") or "?"
            print(f"  #{num} {v['title']} [{v['difficulty']}] 前回習得: {mastered_date}")
            print(f"       開始 → python3 scripts/review.py {num}")
        print()

    if in_prog:
        print("取り組み中")
        for k, v in in_prog:
            num = int(k[1:5])
            print(f"  #{num} {v['title']} [{v['difficulty']}]")
            print(f"       解答後に評価 → python3 scripts/done.py {num}")
        print()

    weak = weak_topics(progress)
    if weak:
        print("弱点パターン (直近評価・未確認・stageから算出)")
        for tag, retries, n in weak:
            print(f"  {tag}: score {retries} / 該当 {n}問")
        print("  新規候補を見る → python3 scripts/recommend_new.py")
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

    summary = readiness_summary(progress)
    print("\n--- 面接準備度")
    for pattern in CORE_PATTERNS:
        stats = summary["patterns"][pattern]
        easy_needed, _ = needs_easy(progress, pattern)
        next_level = "Easy" if easy_needed else "Medium"
        print(
            f"  {pattern:<24} Easy確認 {stats['verified_easy']:>2} / "
            f"Medium成功 {stats['verified_medium']:>2} / 次: {next_level}"
        )
    rate = "記録なし" if summary["good_rate"] is None else f"{summary['good_rate']:.0f}%"
    print(f"  直近10回 Good以上: {rate}")
    print(f"  Medium定着パターン: {summary['medium_ready']} / {len(CORE_PATTERNS)}")


if __name__ == "__main__":
    main()
