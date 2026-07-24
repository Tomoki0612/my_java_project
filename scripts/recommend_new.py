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
from interview_lib import (
    CORE_PATTERNS,
    entry_patterns,
    patterns_for_tags,
    recommended_difficulty,
    weakness_score,
)

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

PATTERN_QUERY_TAG = {
    "Array/String": "Array",
    "Hash Map/Set": "Hash Table",
    "Two Pointers": "Two Pointers",
    "Sliding Window": "Sliding Window",
    "Stack/Queue": "Stack",
    "Linked List": "Linked List",
    "Binary Search": "Binary Search",
    "Prefix Sum/Intervals": "Prefix Sum",
    "Tree/BST": "Tree",
    "Heap": "Heap (Priority Queue)",
    "Graph BFS/DFS": "Graph",
    "Topological Sort": "Topological Sort",
    "Union Find": "Union Find",
    "Recursion/Backtracking": "Backtracking",
    "Dynamic Programming": "Dynamic Programming",
    "Greedy": "Greedy",
}


def topic_slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def registered_numbers(progress):
    numbers = set()
    for key in progress:
        if re.match(r"p\d{4}_", key):
            numbers.add(int(key[1:5]))
    return numbers


def problem_number(key):
    return int(key[1:5])


def in_progress_entries(progress):
    entries = [
        (key, entry)
        for key, entry in progress.items()
        if entry.get("status") == "in_progress" and re.match(r"p\d{4}_", key)
    ]
    entries.sort(key=lambda item: (item[1].get("added_date", ""), problem_number(item[0])))
    return entries


def print_in_progress_warning(entries):
    if not entries:
        return

    print("未完了の問題があります")
    for key, entry in entries:
        number = problem_number(key)
        print(f"  #{number} {entry['title']} [{entry['difficulty']}]")
        print(f"     評価を記録: python3 scripts/done.py {number}")
    print("  新規追加より先に、まず上の問題を終わらせるのがおすすめです。")
    print()


def weak_topics(progress, limit):
    weak = []
    for pattern in CORE_PATTERNS:
        entries = [entry for entry in progress.values() if pattern in entry_patterns(entry)]
        weak.append((pattern, weakness_score(progress, pattern), len(entries)))
    weak.sort(key=lambda item: (-item[1], item[0]))
    return weak[:limit]


def weak_topic_scores(topics):
    scores = {}
    total = sum(max(1, weakness) for _, weakness, _ in topics) or 1
    for rank, (tag, weakness, _) in enumerate(topics):
        rank_bonus = (len(topics) - rank) * 12
        retry_bonus = round((max(1, weakness) / total) * 40, 1)
        scores[tag] = rank_bonus + retry_bonus
    return scores


def topic_entries(progress, tag):
    return [
        entry for entry in progress.values()
        if tag in entry_patterns(entry)
    ]


def recent_topic_results(entries, limit=5):
    history = []
    for entry in entries:
        for item in entry.get("history") or []:
            history.append(item)
    history.sort(key=lambda item: item.get("date", ""), reverse=True)
    return history[:limit]


def recent_topic_counts(progress, limit=8):
    recent = []
    for entry in progress.values():
        history = entry.get("history") or []
        if not history:
            continue
        latest = max(history, key=lambda item: item.get("date", ""))
        recent.append((latest.get("date", ""), entry_patterns(entry)))

    counts = Counter()
    for _, tags in sorted(recent, key=lambda item: item[0], reverse=True)[:limit]:
        for tag in tags:
            counts[tag] += 1
    return counts


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
    recent_done_count = sum(
        1 for item in recent
        if item.get("rating") in ("good", "easy") or item.get("result") == "done"
    )

    if any(
        item.get("rating") == "again" or item.get("result") == "helped"
        for item in recent
    ):
        return "easy", "直近でAgainがあり、基礎固めを優先"

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


def question_tags(q):
    return [t["name"] for t in q.get("topicTags") or []]


def low_number_penalty(number):
    if number <= 20:
        return 8
    if number <= 100:
        return 4
    return 0


def score_candidate(q, source_tag, source_index, weak_scores, recent_counts):
    number = int(q["questionFrontendId"])
    tags = patterns_for_tags(question_tags(q))
    matched = [tag for tag in tags if tag in weak_scores]
    weak_score = sum(weak_scores[tag] for tag in matched)
    fresh_bonus = sum(6 for tag in matched if recent_counts.get(tag, 0) == 0)
    overlap_bonus = max(0, len(matched) - 1) * 14
    source_bonus = max(0, 8 - source_index * 2)
    penalty = low_number_penalty(number)
    score = weak_score + fresh_bonus + overlap_bonus + source_bonus - penalty

    reasons = []
    if matched:
        reasons.append("弱点: " + ", ".join(matched))
    if overlap_bonus:
        reasons.append("複数弱点に一致")
    fresh = [tag for tag in matched if recent_counts.get(tag, 0) == 0]
    if fresh:
        reasons.append("直近少なめ: " + ", ".join(fresh))
    if penalty:
        reasons.append("低番号偏りを少し減点")

    return {
        "question": q,
        "score": round(score, 1),
        "source_tag": source_tag,
        "reasons": reasons,
    }


def print_question(q, indent="  ", score_info=None):
    number = int(q["questionFrontendId"])
    tags = ", ".join(question_tags(q))
    print(f"{indent}#{number} {q['title']} [{q['difficulty']}]")
    if score_info:
        print(f"{indent}   score: {score_info['score']} ({'; '.join(score_info['reasons'])})")
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
        help="候補の難易度。autoなら進捗からトピックごとに判断",
    )
    args = parser.parse_args()

    progress, _ = load_progress()
    print_in_progress_warning(in_progress_entries(progress))

    topics = weak_topics(progress, args.topics)

    registered = registered_numbers(progress)
    weak_scores = weak_topic_scores(topics)
    recent_counts = recent_topic_counts(progress)
    difficulty_label = "Auto" if args.difficulty == "auto" else args.difficulty.capitalize()

    recommendations = []
    scored_candidates = []
    already_shown = set()
    for tag, weakness, solved_count in topics:
        if args.difficulty == "auto":
            difficulty, reason = recommended_difficulty(progress, tag)
        else:
            difficulty, reason = args.difficulty, "手動指定"

        try:
            query_tag = PATTERN_QUERY_TAG[tag]
            candidates = pick_candidates(query_tag, registered, already_shown, args.per_topic, difficulty)
        except Exception as exc:
            recommendations.append({
                "tag": tag,
                "retries": weakness,
                "solved_count": solved_count,
                "difficulty": difficulty,
                "reason": reason,
                "error": str(exc),
                "candidates": [],
                "scored": [],
            })
            continue

        scored = [
            score_candidate(q, tag, index, weak_scores, recent_counts)
            for index, q in enumerate(candidates)
        ]
        scored_candidates.extend(scored)

        recommendations.append({
            "tag": tag,
            "retries": weakness,
            "solved_count": solved_count,
            "difficulty": difficulty,
            "reason": reason,
            "error": None,
            "candidates": candidates,
            "scored": scored,
        })

    scored_candidates.sort(
        key=lambda item: (
            -item["score"],
            int(item["question"]["questionFrontendId"]),
        )
    )
    today = scored_candidates[0] if scored_candidates else None

    print(f"今日の1問 ({difficulty_label} / 未登録 / 無料問題)")
    print()
    if today:
        print_question(today["question"], indent="  ", score_info=today)
        print()
    else:
        print("  候補なし")
        print()

    print("候補一覧")
    print()
    for rec in recommendations:
        print(f"{rec['tag']}  (弱点score {rec['retries']} / 該当 {rec['solved_count']}問)")
        print(f"  推奨難易度: {rec['difficulty'].capitalize()} - {rec['reason']}")
        if rec["error"]:
            print(f"  候補取得に失敗: {rec['error']}")
            print()
            continue
        if not rec["candidates"]:
            print("  候補なし")
            print()
            continue
        for item in sorted(rec["scored"], key=lambda x: -x["score"]):
            print_question(item["question"], score_info=item)
        print()

    if today is None:
        print("候補が出ない場合は難易度を変えてください。例:")
        print("  python3 scripts/recommend_new.py --difficulty medium")


if __name__ == "__main__":
    main()
