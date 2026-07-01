#!/usr/bin/env python3
"""弱点トピックから今日解く新規問題を1問決める。"""
import argparse
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from new_problem import graphql_request
from progress_lib import load_progress

QUESTION_LIST_QUERY = """
query($skip: Int!, $limit: Int!, $filters: QuestionListFilterInput) {
  questionList(
    categorySlug: ""
    skip: $skip
    limit: $limit
    filters: $filters
  ) {
    data {
      questionFrontendId
      title
      titleSlug
      difficulty
      isPaidOnly
      topicTags {
        name
        slug
      }
    }
  }
}
"""


def topic_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def registered_numbers(progress):
    numbers = set()
    for key in progress:
        if re.match(r"p\d{4}_", key):
            numbers.add(int(key[1:5]))
    return numbers


def weak_topics(progress, limit):
    retries_by_topic = Counter()
    count_by_topic = Counter()
    for entry in progress.values():
        for tag in entry.get("topic_tags") or []:
            count_by_topic[tag] += 1
            retries_by_topic[tag] += entry.get("retries", 0) or 0

    weak = [
        (tag, retries_by_topic[tag], count_by_topic[tag])
        for tag in retries_by_topic
        if retries_by_topic[tag] > 0
    ]
    weak.sort(key=lambda x: (-x[1], x[0]))
    return weak[:limit]


def topic_entries(progress, tag):
    return [
        entry for entry in progress.values()
        if tag in (entry.get("topic_tags") or [])
    ]


def recent_topic_results(entries, limit=5):
    history = []
    for entry in entries:
        for item in entry.get("history") or []:
            history.append(item)
    history.sort(key=lambda item: item.get("date", ""), reverse=True)
    return history[:limit]


def choose_difficulty(entries):
    mastered = Counter(
        entry.get("difficulty")
        for entry in entries
        if entry.get("status") == "mastered"
    )
    retries = sum(entry.get("retries", 0) or 0 for entry in entries)
    retry_rate = retries / max(1, len(entries))

    easy_mastered = mastered.get("Easy", 0)
    medium_mastered = mastered.get("Medium", 0)
    recent = recent_topic_results(entries)
    recent_done_count = sum(1 for item in recent if item.get("result") == "done")

    if any(item.get("result") == "helped" for item in recent):
        return "easy", "直近でhelpedがあり、基礎固めを優先"

    if medium_mastered >= 5 and retry_rate <= 0.3 and recent_done_count >= 3:
        return "hard", "Mediumを十分習得済みで、直近も安定している"

    if easy_mastered >= 8 and retry_rate <= 0.8:
        return "medium", "Easyを十分こなしていて、次は少し負荷を上げたい"

    if easy_mastered >= 5 and retry_rate <= 0.5:
        return "medium", "Easyの基礎量があり、リトライ率も低め"

    return "easy", "リトライ率が高め、または基礎量がまだ少ない"


def fetch_candidates(tag, difficulty, limit):
    filters = {"tags": [topic_slug(tag)]}
    if difficulty:
        filters["difficulty"] = difficulty.upper()

    result = graphql_request(
        QUESTION_LIST_QUERY,
        {"skip": 0, "limit": limit, "filters": filters},
    )
    if result.get("errors"):
        messages = "; ".join(e.get("message", "unknown error") for e in result["errors"])
        raise RuntimeError(messages)
    return result["data"]["questionList"]["data"]


def pick_candidates(tag, registered, already_shown, per_topic, difficulty):
    candidates = []
    for q in fetch_candidates(tag, difficulty, limit=50):
        number = int(q["questionFrontendId"])
        if q.get("isPaidOnly") or number in registered or number in already_shown:
            continue
        candidates.append(q)
        already_shown.add(number)
        if len(candidates) >= per_topic:
            break
    return candidates


def print_question(q, indent="  "):
    number = int(q["questionFrontendId"])
    tags = ", ".join(t["name"] for t in q.get("topicTags") or [])
    print(f"{indent}#{number} {q['title']} [{q['difficulty']}]")
    print(f"{indent}   tags: {tags}")
    print(f"{indent}   add: python3 scripts/new_problem.py {number}")


def main():
    parser = argparse.ArgumentParser(description="弱点トピックから今日解く新規問題を1問決める")
    parser.add_argument("--topics", type=int, default=3, help="見る弱点トピック数")
    parser.add_argument("--per-topic", type=int, default=3, help="各トピックの候補数")
    parser.add_argument(
        "--difficulty",
        choices=["auto", "easy", "medium", "hard"],
        default="auto",
        help="候補の難易度。autoなら進捗からトピックごとにEasy/Mediumを判断",
    )
    args = parser.parse_args()

    progress, _ = load_progress()
    topics = weak_topics(progress, args.topics)
    if not topics:
        print("弱点トピックがまだありません。まずは復習で --helped の記録を貯めてください。")
        print("通常の新規追加: python3 scripts/new_problem.py <番号>")
        return

    registered = registered_numbers(progress)
    difficulty_label = "Auto" if args.difficulty == "auto" else args.difficulty.capitalize()

    recommendations = []
    already_shown = set()
    for tag, retries, solved_count in topics:
        if args.difficulty == "auto":
            difficulty, reason = choose_difficulty(topic_entries(progress, tag))
        else:
            difficulty, reason = args.difficulty, "手動指定"

        try:
            candidates = pick_candidates(tag, registered, already_shown, args.per_topic, difficulty)
        except Exception as exc:
            recommendations.append({
                "tag": tag,
                "retries": retries,
                "solved_count": solved_count,
                "difficulty": difficulty,
                "reason": reason,
                "error": str(exc),
                "candidates": [],
            })
            continue

        recommendations.append({
            "tag": tag,
            "retries": retries,
            "solved_count": solved_count,
            "difficulty": difficulty,
            "reason": reason,
            "error": None,
            "candidates": candidates,
        })

    today = next(
        (rec["candidates"][0] for rec in recommendations if rec["candidates"]),
        None,
    )

    print(f"今日の1問 ({difficulty_label} / 未登録 / 無料問題)")
    print()
    if today:
        print_question(today, indent="  ")
        print()
    else:
        print("  候補なし")
        print()

    print("候補一覧")
    print()
    for rec in recommendations:
        print(f"{rec['tag']}  (累計 {rec['retries']} retries / 該当 {rec['solved_count']}問)")
        print(f"  推奨難易度: {rec['difficulty'].capitalize()} - {rec['reason']}")
        if rec["error"]:
            print(f"  候補取得に失敗: {rec['error']}")
            print()
            continue
        if not rec["candidates"]:
            print("  候補なし")
            print()
            continue
        for q in rec["candidates"]:
            print_question(q)
        print()

    if today is None:
        print("候補が出ない場合は難易度を変えてください。例:")
        print("  python3 scripts/recommend_new.py --difficulty medium")


if __name__ == "__main__":
    main()
