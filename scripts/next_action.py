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

    # 優先度: 復習中 > 取り組み中 > 長期復習 > 新規問題追加
    # 復習中はリトライ多い順 → next_review 古い順 で弱点優先
    if short_reviews:
        short_reviews.sort(key=lambda x: (-x[1].get("retries", 0), x[1].get("next_review", "")))
        k, v = short_reviews[0]
        num = int(k[1:5])
        return {
            "kind": "review",
            "number": num,
            "title": v["title"],
            "command": f"python3 scripts/review.py {num}",
            "hint": f"復習: #{num} {v['title']} [{v['difficulty']}] stage {v.get('stage', 0)}",
        }

    if in_prog:
        k, v = in_prog[0]
        num = int(k[1:5])
        return {
            "kind": "in_progress",
            "number": num,
            "title": v["title"],
            "command": f"python3 scripts/done.py {num}",
            "hint": f"取り組み中: #{num} {v['title']} [{v['difficulty']}] — 解けたら done / 詰まったら done --helped",
        }

    if long_reviews:
        long_reviews.sort(key=lambda x: x[1].get("next_review", ""))
        k, v = long_reviews[0]
        num = int(k[1:5])
        return {
            "kind": "long_review",
            "number": num,
            "title": v["title"],
            "command": f"python3 scripts/review.py {num}",
            "hint": f"長期復習: #{num} {v['title']} [{v['difficulty']}] (前回習得 {v.get('mastered_date', '?')})",
        }

    return {
        "kind": "new_problem",
        "number": None,
        "title": None,
        "command": "python3 scripts/new_problem.py <番号> --ja",
        "hint": "新しい問題を追加しましょう",
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
