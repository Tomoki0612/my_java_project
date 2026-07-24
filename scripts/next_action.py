"""次にやるべき1アクションを決める共通ロジック"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from progress_lib import load_progress


def pick_next(progress, today_iso=None):
    """進捗から「次の1アクション」を返す。

    Returns: dict with keys {kind, number, title, command, hint} or None
    """
    if today_iso is None:
        today_iso = date.today().isoformat()

    short_reviews = []
    long_reviews = []
    in_prog = []
    for k, v in progress.items():
        nr = v.get("next_review")
        status = v.get("status")
        if status == "in_progress":
            in_prog.append((k, v))
        elif nr and nr <= today_iso:
            if status == "mastered":
                long_reviews.append((k, v))
            else:
                short_reviews.append((k, v))

    # 優先度: 期限復習（短期・長期） > 取り組み中 > 新規問題追加。
    if short_reviews or long_reviews:
        due = [(k, v, "review") for k, v in short_reviews]
        due += [(k, v, "long_review") for k, v in long_reviews]
        due.sort(key=lambda x: (x[1].get("next_review", ""), x[1].get("stage", 0)))
        k, v, kind = due[0]
        num = int(k[1:5])
        label = "長期復習" if kind == "long_review" else "復習"
        return {
            "kind": kind,
            "number": num,
            "title": v["title"],
            "command": f"python3 scripts/review.py {num}",
            "hint": f"{label}: #{num} {v['title']} [{v['difficulty']}] stage {v.get('stage', 0)}",
        }

    if in_prog:
        k, v = in_prog[0]
        num = int(k[1:5])
        return {
            "kind": "in_progress",
            "number": num,
            "title": v["title"],
            "command": f"python3 scripts/done.py {num}",
            "hint": f"取り組み中: #{num} {v['title']} [{v['difficulty']}] — 解答後に4段階評価",
        }

    return {
        "kind": "recommend_new",
        "number": None,
        "title": None,
        "command": "python3 scripts/recommend_new.py",
        "hint": "面接パターン別の実力から今日の1問を決めましょう",
    }


def format_one_line(action):
    if action is None:
        return "次のアクション: (なし)"
    return f">>> 次: {action['hint']}\n    $ {action['command']}"


def main():
    progress, _ = load_progress()
    action = pick_next(progress)
    print(format_one_line(action))


if __name__ == "__main__":
    main()
