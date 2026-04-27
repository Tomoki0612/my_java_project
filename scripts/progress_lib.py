"""progress.json の読み書き・マイグレーション・ステージ遷移を扱う共通モジュール"""
import json
import os
from datetime import date, timedelta

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src", "main", "java", "leetcode")
PROGRESS_FILE = os.path.join(SRC_ROOT, "progress.json")

# 間隔反復: ステージ -> 次回復習までの日数
INTERVALS_DAYS = [1, 3, 7, 21, 60, 180]
MAX_STAGE = len(INTERVALS_DAYS) - 1


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


def apply_transition(entry, helped, today=None):
    """done / --helped の結果をエントリに反映する。"""
    if today is None:
        today = date.today()

    cur_stage = entry.get("stage")

    if helped:
        new_stage = 0
        entry["retries"] = entry.get("retries", 0) + 1
    elif cur_stage is None:
        # 初回 in_progress を自力突破 → 一気に最終ステージ（長期復習サイクルへ）
        new_stage = MAX_STAGE
    else:
        new_stage = min(cur_stage + 1, MAX_STAGE)

    entry["stage"] = new_stage
    entry["next_review"] = (today + timedelta(days=INTERVALS_DAYS[new_stage])).isoformat()

    if new_stage == MAX_STAGE:
        entry["status"] = "mastered"
        if not entry.get("mastered_date"):
            entry["mastered_date"] = today.isoformat()
    else:
        entry["status"] = "review"

    history = entry.setdefault("history", [])
    history.append({
        "date":   today.isoformat(),
        "result": "helped" if helped else "done",
        "stage":  new_stage,
    })
