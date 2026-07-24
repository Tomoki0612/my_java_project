"""progress.json の読み書き・マイグレーション・学習評価を扱う共通モジュール。"""
import json
import os
from collections import Counter
from datetime import date, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src", "main", "java", "leetcode")
PROGRESS_FILE = os.path.join(SRC_ROOT, "progress.json")

# 間隔反復: ステージ -> 次回復習までの日数
INTERVALS_DAYS = [1, 3, 7, 21, 60, 180]
INTERVAL_FLEX_DAYS = [0, 0, 1, 2, 4, 7]
MAX_STAGE = len(INTERVALS_DAYS) - 1
RATINGS = ("again", "hard", "good", "easy")


def normalize_rating(rating):
    value = (rating or "").strip().lower()
    aliases = {"a": "again", "h": "hard", "g": "good", "e": "easy"}
    value = aliases.get(value, value)
    if value not in RATINGS:
        raise ValueError(f"rating は {', '.join(RATINGS)} のいずれかです")
    return value


def _migrate_history(entry):
    """旧 result/stage 履歴に新しい評価フィールドを追記する。"""
    dirty = False
    previous_stage = None
    for item in entry.setdefault("history", []):
        if "rating" not in item:
            item["rating"] = "again" if item.get("result") == "helped" else "good"
            dirty = True
        if "stage_before" not in item:
            item["stage_before"] = previous_stage
            dirty = True
        if "stage_after" not in item:
            item["stage_after"] = item.get("stage")
            dirty = True
        previous_stage = item.get("stage_after")
    return dirty


def _migrate_entry(entry, today):
    """旧スキーマのエントリに足りないフィールドを補完する。変更があれば True。"""
    dirty = False

    if "stage" not in entry:
        status = entry.get("status")
        if status == "mastered":
            entry["stage"] = MAX_STAGE
            base = entry.get("mastered_date") or today.isoformat()
            try:
                base_d = date.fromisoformat(base)
            except ValueError:
                base_d = today
            entry["next_review"] = (base_d + timedelta(days=INTERVALS_DAYS[MAX_STAGE])).isoformat()
        elif status == "review":
            entry["stage"] = 0
            if not entry.get("next_review"):
                entry["next_review"] = (today + timedelta(days=INTERVALS_DAYS[0])).isoformat()
        else:
            entry["stage"] = None
            entry["next_review"] = None
        dirty = True

    if "topic_tags" not in entry:
        entry["topic_tags"] = []
        dirty = True

    if "history" not in entry:
        entry["history"] = []
        dirty = True

    if _migrate_history(entry):
        dirty = True

    if "last_rating" not in entry:
        history = entry.get("history") or []
        entry["last_rating"] = history[-1].get("rating") if history else None
        dirty = True

    # 履歴のない一括import済み問題は、現在の実力としては未確認扱い。
    if "verified" not in entry:
        entry["verified"] = any(
            item.get("rating") in ("good", "easy") for item in entry.get("history") or []
        )
        dirty = True

    return dirty


def load_progress():
    """progress.json を読み、未マイグレーションのエントリを補完する。

    Returns: (progress dict, dirty bool) — dirty=True なら呼び出し側で save_progress すべき。
    """
    if not os.path.exists(PROGRESS_FILE):
        return {}, False
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        progress = json.load(f)

    today = date.today()
    dirty = False
    for entry in progress.values():
        if _migrate_entry(entry, today):
            dirty = True
    return progress, dirty


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def find_key(progress, number):
    prefix = f"p{number:04d}_"
    for key in progress:
        if key.startswith(prefix):
            return key
    return None


def _scheduled_counts(progress):
    return Counter(
        entry.get("next_review")
        for entry in (progress or {}).values()
        if entry.get("next_review")
    )


def choose_review_date(stage, today, progress=None):
    """目標間隔の許容範囲内で、予定件数が最も少ない日を選ぶ。"""
    target = today + timedelta(days=INTERVALS_DAYS[stage])
    flex = INTERVAL_FLEX_DAYS[stage]
    if flex == 0:
        return target

    counts = _scheduled_counts(progress)
    candidates = [target + timedelta(days=offset) for offset in range(-flex, flex + 1)]
    return min(candidates, key=lambda candidate: (counts[candidate.isoformat()], candidate))


def next_stage(current_stage, rating):
    """4段階評価から次stageを返す純粋関数。"""
    rating = normalize_rating(rating)
    if current_stage is None:
        return {"again": 0, "hard": 0, "good": 1, "easy": 2}[rating]
    if rating == "again":
        return 0
    if rating == "hard":
        return max(0, current_stage - 1)
    step = 1 if rating == "good" else 2
    return min(MAX_STAGE, current_stage + step)


def apply_transition(
    entry,
    rating=None,
    today=None,
    progress=None,
):
    """4段階評価をエントリへ反映する。"""
    if today is None:
        today = date.today()
    rating = normalize_rating(rating)

    cur_stage = entry.get("stage")
    new_stage = next_stage(cur_stage, rating)
    if rating == "again":
        entry["retries"] = entry.get("retries", 0) + 1

    entry["stage"] = new_stage
    entry["next_review"] = choose_review_date(new_stage, today, progress).isoformat()
    entry["last_rating"] = rating
    if rating in ("good", "easy"):
        entry["verified"] = True

    if new_stage == MAX_STAGE:
        entry["status"] = "mastered"
        if not entry.get("mastered_date"):
            entry["mastered_date"] = today.isoformat()
    else:
        entry["status"] = "review"

    history = entry.setdefault("history", [])
    history.append({
        "date": today.isoformat(),
        "rating": rating,
        "stage_before": cur_stage,
        "stage_after": new_stage,
    })
    return new_stage
