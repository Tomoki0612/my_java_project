import unittest

from scripts.interview_lib import (
    needs_easy,
    patterns_for_tags,
    readiness_summary,
    recommended_difficulty,
)


def solved_entry(number, difficulty="Easy", rating="good", minutes=20):
    return {
        "title": str(number),
        "difficulty": difficulty,
        "status": "review",
        "stage": 2,
        "verified": rating in ("good", "easy"),
        "topic_tags": ["Hash Table"],
        "history": [
            {
                "date": f"2026-01-{number:02d}",
                "rating": rating,
                "duration_minutes": minutes,
                "reflection": {
                    "pattern": "Hash Map/Set",
                    "complexity": "時間 O(n) / 空間 O(n)",
                    "lesson": "なし",
                },
            }
        ],
    }


class InterviewCurriculumTest(unittest.TestCase):
    def test_topic_tags_map_to_interview_patterns(self):
        patterns = patterns_for_tags(["Array", "Hash Table", "Two Pointers"])
        self.assertIn("Array/String", patterns)
        self.assertIn("Hash Map/Set", patterns)
        self.assertIn("Two Pointers", patterns)

    def test_two_verified_easy_unlock_medium(self):
        progress = {"one": solved_entry(1), "two": solved_entry(2)}
        self.assertEqual((False, "Easy基礎を確認済み"), needs_easy(progress, "Hash Map/Set"))
        self.assertEqual("medium", recommended_difficulty(progress, "Hash Map/Set")[0])

    def test_recent_again_returns_to_easy(self):
        progress = {
            "one": solved_entry(1),
            "two": solved_entry(2),
            "three": solved_entry(3, difficulty="Medium", rating="again", minutes=40),
        }
        self.assertTrue(needs_easy(progress, "Hash Map/Set")[0])

    def test_slow_easy_stays_on_easy(self):
        progress = {"one": solved_entry(1, minutes=30), "two": solved_entry(2, minutes=28)}
        self.assertTrue(needs_easy(progress, "Hash Map/Set")[0])

    def test_readiness_reports_medians_and_good_rate(self):
        progress = {"one": solved_entry(1, minutes=18), "two": solved_entry(2, minutes=22)}
        summary = readiness_summary(progress)
        self.assertEqual(20, summary["easy_median"])
        self.assertEqual(100, summary["good_rate"])


if __name__ == "__main__":
    unittest.main()
