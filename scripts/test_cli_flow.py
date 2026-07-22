import unittest

from scripts.done import collect_reflection, parse_args
from scripts.next_action import pick_next


class DoneCliTest(unittest.TestCase):
    def test_non_interactive_reflection(self):
        args = parse_args(
            [
                "203",
                "--rating",
                "good",
                "--minutes",
                "20",
                "--pattern",
                "Linked List",
                "--complexity",
                "時間 O(n) / 空間 O(1)",
                "--lesson",
                "sentinelを使う",
            ]
        )
        self.assertEqual(
            ("good", 20, "Linked List", "時間 O(n) / 空間 O(1)", "sentinelを使う"),
            collect_reflection(args),
        )

    def test_helped_conflicts_with_other_rating(self):
        args = parse_args(
            [
                "203", "--helped", "--rating", "easy", "--minutes", "10",
                "--pattern", "x", "--complexity", "O(n)", "--lesson", "x",
            ]
        )
        with self.assertRaises(ValueError):
            collect_reflection(args)


class DailyQueueTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
