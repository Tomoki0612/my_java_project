import unittest
from datetime import datetime, timezone
from io import StringIO
from unittest.mock import Mock, call, patch

from scripts.done import (
    auto_commit_and_push,
    build_completion_guidance,
    collect_rating,
    parse_args,
)
from scripts.next_action import due_review_actions, pick_next
from scripts.progress_lib import apply_transition
from scripts.today import main as today_main
from scripts.recommend_new import main as recommend_main


class DoneCliTest(unittest.TestCase):
    def test_non_interactive_rating(self):
        args = parse_args(["203", "--rating", "good"])
        self.assertEqual("good", collect_rating(args))

    @patch("scripts.done.run_git")
    def test_auto_commit_and_push_only_targets_solution_test_and_progress(self, run_git):
        run_git.side_effect = [
            _git_result(),
            _git_result(),
            _git_result("src/main/java/leetcode/p0203_remove_linked_list_elements/Solution.java\n"
                        "src/test/java/leetcode/p0203_remove_linked_list_elements/SolutionTest.java\n"
                        "src/main/java/leetcode/progress.json\n"),
            _git_result(),
            _git_result(),
        ]

        self.assertTrue(
            auto_commit_and_push(
                "p0203_remove_linked_list_elements",
                203,
                "Remove Linked List Elements",
                "good",
            )
        )
        self.assertEqual(
            call(
                "add",
                "--",
                "src/main/java/leetcode/p0203_remove_linked_list_elements/Solution.java",
                "src/test/java/leetcode/p0203_remove_linked_list_elements/SolutionTest.java",
                "src/main/java/leetcode/progress.json",
            ),
            run_git.call_args_list[1],
        )
        self.assertEqual(call("push"), run_git.call_args_list[-1])


def _git_result(stdout="", stderr="", returncode=0):
    result = Mock()
    result.stdout = stdout
    result.stderr = stderr
    result.returncode = returncode
    return result


class DailyQueueTest(unittest.TestCase):
    def test_completed_day_stops_recommendations_until_tomorrow(self):
        for status, stage in (("in_progress", None), ("review", 2), ("mastered", 5)):
            for rating in ("again", "hard", "good", "easy"):
                with self.subTest(status=status, rating=rating):
                    entry = {
                        "title": "Completed", "difficulty": "Easy",
                        "status": status, "stage": stage, "history": [],
                    }
                    progress = {"p0001_completed": entry}
                    apply_transition(entry, rating, now=datetime(2026, 1, 2, 12, tzinfo=timezone.utc))
                    self.assertIsNone(pick_next(progress, "2026-01-02"))
                    self.assertIn("今日の学習は終了", build_completion_guidance(
                        progress, status != "in_progress", "2026-01-02"
                    )[-1])
                    # 翌日は期限があれば復習、それ以外は新規を案内する。
                    self.assertIsNotNone(pick_next(progress, "2026-01-03"))
                    if entry["next_review"] > "2026-01-03":
                        self.assertEqual("recommend_new", pick_next(progress, "2026-01-03")["kind"])

    def test_completed_day_still_prioritizes_due_and_unfinished_work(self):
        progress = {
            "p0001_done": {
                "status": "review", "next_review": "2026-01-09",
                "history": [{"date": "2026-01-02", "rating": "good"}],
            },
            "p0002_work": {
                "title": "Work", "difficulty": "Easy", "status": "in_progress",
            },
            "p0003_due": {
                "title": "Due", "difficulty": "Easy", "status": "review",
                "stage": 0, "next_review": "2026-01-02",
            },
        }
        self.assertEqual("review", pick_next(progress, "2026-01-02")["kind"])
        del progress["p0003_due"]
        self.assertEqual("in_progress", pick_next(progress, "2026-01-02")["kind"])
        self.assertIn("取り組み中", build_completion_guidance(progress, True, "2026-01-02")[0])

    def test_completed_day_cli_output_does_not_offer_more_problems(self):
        from datetime import date
        progress = {"p0001_done": {
            "title": "Done", "difficulty": "Easy", "status": "review", "stage": 1,
            "topic_tags": ["Array"], "history": [{"date": date.today().isoformat(), "rating": "good"}],
        }}
        with patch("scripts.today.load_progress", return_value=(progress, False)), patch(
            "sys.stdout", new_callable=StringIO
        ) as output:
            today_main()
        self.assertIn("今日の学習は終了", output.getvalue())
        self.assertNotIn("scripts/recommend_new.py", output.getvalue())

        with patch("scripts.recommend_new.load_progress", return_value=(progress, False)), patch(
            "sys.argv", ["recommend_new.py"]
        ), patch("scripts.recommend_new.fetch_candidates") as fetch, patch(
            "sys.stdout", new_callable=StringIO
        ) as output:
            recommend_main()
        self.assertIn("今日の学習は終了", output.getvalue())
        fetch.assert_not_called()

    def test_all_due_reviews_precede_in_progress(self):
        progress = {
            "p0001_old_mastered": {
                "title": "Old",
                "difficulty": "Easy",
                "status": "mastered",
                "stage": 5,
                "next_review": "2026-01-01",
            },
            "p0002_work": {
                "title": "Work",
                "difficulty": "Easy",
                "status": "in_progress",
                "stage": None,
                "next_review": None,
            },
        }
        self.assertEqual("long_review", pick_next(progress, "2026-01-02")["kind"])

    def test_new_recommendation_is_used_when_queue_empty(self):
        self.assertEqual("recommend_new", pick_next({}, "2026-01-02")["kind"])

    def test_due_review_actions_returns_all_reviews_in_priority_order(self):
        progress = {
            "p0001_later": {
                "title": "Later",
                "difficulty": "Easy",
                "status": "review",
                "stage": 1,
                "next_review": "2026-01-02",
            },
            "p0002_earlier": {
                "title": "Earlier",
                "difficulty": "Medium",
                "status": "review",
                "stage": 2,
                "next_review": "2026-01-01",
            },
        }
        actions = due_review_actions(progress, "2026-01-02")
        self.assertEqual([2, 1], [action["number"] for action in actions])

    def test_completion_guidance_shows_remaining_review_count_and_next_problem(self):
        progress = {
            "p0001_completed": {
                "title": "Completed",
                "difficulty": "Easy",
                "status": "review",
                "stage": 2,
                "next_review": "2026-01-09",
            },
            "p0002_due": {
                "title": "Due",
                "difficulty": "Medium",
                "status": "review",
                "stage": 1,
                "next_review": "2026-01-01",
            },
            "p0003_due": {
                "title": "Also Due",
                "difficulty": "Easy",
                "status": "review",
                "stage": 0,
                "next_review": "2026-01-02",
            },
        }
        guidance = build_completion_guidance(progress, True, "2026-01-02")
        self.assertEqual("今日の期限復習はあと 2問です。", guidance[0])
        self.assertIn("#2 Due", guidance[1])
        self.assertIn("python3 scripts/review.py 2", guidance[1])

    def test_completion_guidance_marks_review_queue_complete(self):
        progress = {
            "p0001_completed": {
                "title": "Completed",
                "difficulty": "Easy",
                "status": "review",
                "stage": 2,
                "next_review": "2026-01-09",
            },
        }
        self.assertEqual(
            [
                "今日の期限復習はすべて完了しました。",
                "今日の学習は終了です。お疲れさまでした！",
            ],
            build_completion_guidance(progress, True, "2026-01-02"),
        )

    def test_completion_guidance_marks_daily_new_problem_complete(self):
        self.assertEqual(
            [
                "今日の新規問題1問は完了しました。",
                "今日の学習は終了です。お疲れさまでした！",
            ],
            build_completion_guidance({}, False, "2026-01-02"),
        )


if __name__ == "__main__":
    unittest.main()
