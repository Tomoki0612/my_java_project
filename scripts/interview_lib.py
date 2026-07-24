"""コーディング面接向けのパターン分類と習熟度集計。"""
PATTERN_TAGS = {
    "Array/String": {"Array", "String", "Matrix", "Simulation"},
    "Hash Map/Set": {"Hash Table", "Counting"},
    "Two Pointers": {"Two Pointers"},
    "Sliding Window": {"Sliding Window"},
    "Stack/Queue": {"Stack", "Queue", "Monotonic Stack", "Monotonic Queue"},
    "Linked List": {"Linked List"},
    "Binary Search": {"Binary Search"},
    "Prefix Sum/Intervals": {"Prefix Sum", "Line Sweep", "Sorting"},
    "Tree/BST": {"Tree", "Binary Tree", "Binary Search Tree"},
    "Heap": {"Heap (Priority Queue)"},
    "Graph BFS/DFS": {"Graph", "Breadth-First Search", "Depth-First Search"},
    "Topological Sort": {"Topological Sort"},
    "Union Find": {"Union Find"},
    "Recursion/Backtracking": {"Recursion", "Backtracking", "Divide and Conquer"},
    "Dynamic Programming": {"Dynamic Programming", "Memoization"},
    "Greedy": {"Greedy"},
}

CORE_PATTERNS = tuple(PATTERN_TAGS)


def patterns_for_tags(tags):
    tags = set(tags or [])
    return [name for name, known_tags in PATTERN_TAGS.items() if tags & known_tags]


def entry_patterns(entry):
    return patterns_for_tags(entry.get("topic_tags"))


def latest_attempt(entry):
    history = entry.get("history") or []
    return history[-1] if history else None


def _successful(entry):
    attempt = latest_attempt(entry)
    return bool(entry.get("verified") and attempt and attempt.get("rating") in ("good", "easy"))


def pattern_stats(progress, pattern):
    entries = [entry for entry in progress.values() if pattern in entry_patterns(entry)]
    verified_easy = [entry for entry in entries if entry.get("difficulty") == "Easy" and _successful(entry)]
    verified_medium = [entry for entry in entries if entry.get("difficulty") == "Medium" and _successful(entry)]

    recent = []
    for entry in entries:
        for attempt in entry.get("history") or []:
            recent.append((attempt.get("date", ""), attempt))
    recent_attempts = [
        attempt for _, attempt in sorted(recent, key=lambda item: item[0], reverse=True)[:3]
    ]

    return {
        "entries": entries,
        "verified_easy": len(verified_easy),
        "verified_medium": len(verified_medium),
        "recent": recent_attempts,
    }


def needs_easy(progress, pattern):
    stats = pattern_stats(progress, pattern)
    ratings = [attempt.get("rating") for attempt in stats["recent"]]
    if stats["verified_easy"] < 2:
        return True, "確認済みEasyが2問未満"
    if "again" in ratings:
        return True, "直近3回にAgainあり"
    if ratings and ratings[0] == "hard":
        return True, "直近評価がHard"
    return False, "Easy基礎を確認済み"


def recommended_difficulty(progress, pattern):
    easy, reason = needs_easy(progress, pattern)
    return ("easy", reason) if easy else ("medium", reason)


def weakness_score(progress, pattern):
    stats = pattern_stats(progress, pattern)
    score = max(0, 2 - stats["verified_easy"]) * 8
    weights = {"again": 12, "hard": 6, "good": -2, "easy": -4}
    for index, attempt in enumerate(stats["recent"]):
        score += weights.get(attempt.get("rating"), 0) * (3 - index)
    entries = stats["entries"]
    if entries:
        unverified_rate = sum(not entry.get("verified") for entry in entries) / len(entries)
        low_stage = [max(0, 3 - entry["stage"]) for entry in entries if entry.get("stage") is not None]
        score += round(unverified_rate * 8, 1)
        score += round(sum(low_stage) / max(1, len(low_stage)), 1)
    return round(score, 1)


def readiness_summary(progress):
    per_pattern = {pattern: pattern_stats(progress, pattern) for pattern in CORE_PATTERNS}
    recent = []
    for entry in progress.values():
        for attempt in entry.get("history") or []:
            recent.append((attempt.get("date", ""), attempt, entry.get("difficulty")))
    recent_ten = sorted(recent, key=lambda item: item[0], reverse=True)[:10]
    good = sum(attempt.get("rating") in ("good", "easy") for _, attempt, _ in recent_ten)
    return {
        "patterns": per_pattern,
        "good_rate": (good / len(recent_ten) * 100) if recent_ten else None,
        "medium_ready": sum(stats["verified_medium"] >= 3 for stats in per_pattern.values()),
    }
