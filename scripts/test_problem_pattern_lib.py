import unittest

from scripts.problem_pattern_lib import (
    needs_easy,
    pattern_stats,
    patterns_for_tags,
    readiness_summary,
    recommended_difficulty,
)


def solved_entry(number, difficulty="Easy", rating="good"):
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
            }
        ],
    }


class ProblemPatternCurriculumTest(unittest.TestCase):
    def test_latest_same_day_hard_returns_to_easy_regardless_of_problem_order(self):
        progress = {"one": solved_entry(1), "two": solved_entry(2), "three": solved_entry(3)}
        for hour, entry in enumerate(progress.values(), start=10):
            entry["history"][0].update({
                "date": "2026-01-03",
                "recorded_at": f"2026-01-03T{hour}:00:00+09:00",
            })
        progress["one"]["history"].append({
            "date": "2026-01-03", "rating": "hard",
            "recorded_at": "2026-01-03T13:00:00+09:00",
        })
        for ordered in (progress, dict(reversed(list(progress.items())))):
            self.assertEqual((True, "直近評価がHard"), needs_easy(ordered, "Hash Map/Set"))
            self.assertEqual("easy", recommended_difficulty(ordered, "Hash Map/Set")[0])

    def test_recent_ten_excludes_earlier_same_day_failure(self):
        entry = solved_entry(1)
        entry["history"] = [
            {
                "date": "2026-01-01", "rating": "again" if hour == 0 else "good",
                "recorded_at": f"2026-01-01T{hour:02d}:00:00+09:00",
            }
            for hour in range(11)
        ]
        self.assertEqual(100, readiness_summary({"one": entry})["good_rate"])

    def test_topic_tags_map_to_problem_patterns(self):
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
            "three": solved_entry(3, difficulty="Medium", rating="again"),
        }
        self.assertTrue(needs_easy(progress, "Hash Map/Set")[0])

    def test_five_verified_medium_with_stable_recent_results_unlock_hard(self):
        progress = {
            "easy-one": solved_entry(1),
            "easy-two": solved_entry(2),
            **{
                f"medium-{number}": solved_entry(number, difficulty="Medium")
                for number in range(3, 8)
            },
        }
        self.assertEqual("hard", recommended_difficulty(progress, "Hash Map/Set")[0])

    def test_lifetime_retries_do_not_prevent_promotion_after_recent_success(self):
        progress = {
            "easy-one": solved_entry(1),
            "easy-two": solved_entry(2),
            **{
                f"medium-{number}": solved_entry(number, difficulty="Medium")
                for number in range(3, 8)
            },
        }
        progress["medium-3"]["retries"] = 100
        self.assertEqual("hard", recommended_difficulty(progress, "Hash Map/Set")[0])

    def test_retry_rate_threshold_uses_recent_ten_attempts(self):
        for failures, expected in ((3, "hard"), (4, "medium")):
            with self.subTest(failures=failures):
                progress = {
                    "easy-one": solved_entry(1), "easy-two": solved_entry(2),
                    **{f"medium-{n}": solved_entry(n, difficulty="Medium") for n in range(3, 8)},
                }
                # 同日の評価を時刻順に並べ、直近3回は成功にする。
                progress["medium-3"]["history"].extend([
                    {
                        "date": "2026-02-01",
                        "recorded_at": f"2026-02-01T{hour:02d}:00:00+09:00",
                        "rating": "again" if hour < failures else "good",
                    }
                    for hour in range(10)
                ])
                self.assertEqual(failures / 10, pattern_stats(progress, "Hash Map/Set")["retry_rate"])
                self.assertEqual(expected, recommended_difficulty(progress, "Hash Map/Set")[0])

                # 古いAgainが窓から外れると、直近10回の実力だけで昇格する。
                progress["medium-3"]["history"].append({
                    "date": "2026-02-02", "rating": "good",
                })
                self.assertEqual((failures - 1) / 10, pattern_stats(progress, "Hash Map/Set")["retry_rate"])
                self.assertEqual("hard", recommended_difficulty(progress, "Hash Map/Set")[0])

    def test_retry_rate_uses_available_history_and_excludes_other_patterns(self):
        entry = solved_entry(1)
        entry["history"] = [
            {"date": "2026-01-01", "rating": rating}
            for rating in ("again", "hard", "good", "easy")
        ]
        progress = {
            "one": entry,
            "legacy": {"topic_tags": ["Hash Table"], "retries": 99, "history": []},
            "other": {"topic_tags": ["Tree"], "history": [{"date": "2026-02-01", "rating": "again"}]},
        }
        self.assertEqual(0.25, pattern_stats(progress, "Hash Map/Set")["retry_rate"])
        self.assertIsNone(pattern_stats({}, "Hash Map/Set")["retry_rate"])

    def test_readiness_reports_good_rate(self):
        progress = {"one": solved_entry(1), "two": solved_entry(2)}
        summary = readiness_summary(progress)
        self.assertEqual(100, summary["good_rate"])


if __name__ == "__main__":
    unittest.main()
