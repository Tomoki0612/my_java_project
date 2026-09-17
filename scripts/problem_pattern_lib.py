"""問題パターンの分類と習熟度集計。"""
if __package__:
    from .progress_lib import recent_attempts
else:
    from progress_lib import recent_attempts


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
RETRY_WINDOW = 10


def patterns_for_tags(tags):
    tags = set(tags or [])
    return [name for name, known_tags in PATTERN_TAGS.items() if tags & known_tags]


def entry_patterns(entry):
    return patterns_for_tags(entry.get("topic_tags"))


def latest_attempt(entry):
    history = recent_attempts([entry], limit=1)
    return history[0] if history else None


def _successful(entry):
    attempt = latest_attempt(entry)
    return bool(entry.get("verified") and attempt and attempt.get("rating") in ("good", "easy"))


def pattern_stats(progress, pattern):
    entries = [entry for entry in progress.values() if pattern in entry_patterns(entry)]
    verified_easy = [entry for entry in entries if entry.get("difficulty") == "Easy" and _successful(entry)]
    verified_medium = [entry for entry in entries if entry.get("difficulty") == "Medium" and _successful(entry)]
    attempts = recent_attempts(entries, limit=RETRY_WINDOW)
    retry_rate = (
        sum(attempt.get("rating") == "again" for attempt in attempts) / len(attempts)
        if attempts else None
    )

    return {
        "entries": entries,
        "verified_easy": len(verified_easy),
        "verified_medium": len(verified_medium),
        "recent": attempts[:3],
        "retry_rate": retry_rate,
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
    if easy:
        return "easy", reason

    stats = pattern_stats(progress, pattern)
    recent_ratings = [attempt.get("rating") for attempt in stats["recent"]]
    retry_rate = stats["retry_rate"]
    if (
        stats["verified_medium"] >= 5
        and retry_rate is not None
        and retry_rate <= 0.3
        and len(recent_ratings) >= 3
        and all(rating in ("good", "easy") for rating in recent_ratings)
    ):
        return "hard", "確認済みMediumが5問以上で、直近3回も安定"

    return "medium", reason


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
    recent_ten = recent_attempts(progress.values(), limit=10)
    good = sum(attempt.get("rating") in ("good", "easy") for attempt in recent_ten)
    return {
        "patterns": per_pattern,
        "good_rate": (good / len(recent_ten) * 100) if recent_ten else None,
        "medium_ready": sum(stats["verified_medium"] >= 3 for stats in per_pattern.values()),
    }
