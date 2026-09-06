import unittest
from datetime import date, datetime, timedelta, timezone

from scripts.progress_lib import (
    _migrate_entry,
    apply_transition,
    choose_review_date,
    next_stage,
    recent_attempts,
)


class StageTransitionTest(unittest.TestCase):
    def test_timestamp_and_learning_date_use_the_same_local_clock(self):
        now = datetime(2026, 1, 2, 0, 1, tzinfo=timezone(timedelta(hours=9)))
        entry = {"stage": None, "history": []}
        apply_transition(entry, "good", now=now)
        attempt = entry["history"][0]
        self.assertEqual("2026-01-02", attempt["date"])
        self.assertEqual(now.isoformat(), attempt["recorded_at"])

    def test_initial_ratings_do_not_jump_to_mastered(self):
        self.assertEqual(0, next_stage(None, "again"))
        self.assertEqual(0, next_stage(None, "hard"))
        self.assertEqual(1, next_stage(None, "good"))
        self.assertEqual(2, next_stage(None, "easy"))

    def test_review_ratings_respect_bounds(self):
        self.assertEqual(0, next_stage(0, "hard"))
        self.assertEqual(0, next_stage(4, "again"))
        self.assertEqual(3, next_stage(4, "hard"))
        self.assertEqual(5, next_stage(4, "good"))
        self.assertEqual(5, next_stage(4, "easy"))

    def test_apply_transition_records_rating(self):
        entry = {
            "status": "in_progress",
            "stage": None,
            "history": [],
            "retries": 0,
        }
        progress = {"p0001_two_sum": entry}
        apply_transition(
            entry,
            "good",
            today=date(2026, 1, 1),
            progress=progress,
        )
        self.assertEqual(1, entry["stage"])
        self.assertEqual("review", entry["status"])
        self.assertTrue(entry["verified"])
        self.assertEqual("2026-01-04", entry["next_review"])
        self.assertEqual("good", entry["history"][-1]["rating"])
        self.assertNotIn("reflection", entry["history"][-1])

    def test_again_increments_retries_and_resets(self):
        entry = {"status": "review", "stage": 3, "history": [], "retries": 1}
        apply_transition(entry, "again", today=date(2026, 1, 1))
        self.assertEqual(0, entry["stage"])
        self.assertEqual(2, entry["retries"])
        self.assertFalse(entry.get("verified", False))


class SchedulingAndMigrationTest(unittest.TestCase):
    def test_mixed_history_uses_time_and_preserves_legacy_append_order(self):
        older = {"date": "2026-01-02", "rating": "good"}
        later = {"date": "2026-01-02", "rating": "hard"}
        timed = {
            "date": "2026-01-02", "rating": "easy",
            "recorded_at": "2026-01-02T10:00:00+09:00",
        }
        entries = [{"history": [older, later]}, {"history": [timed]}]
        self.assertEqual([timed, later, older], recent_attempts(entries))
        self.assertNotIn("recorded_at", older)

    def test_timestamps_compare_instants_across_timezone_offsets(self):
        first = {"date": "2026-01-02", "recorded_at": "2026-01-02T10:00:00+09:00"}
        last = {"date": "2026-01-02", "recorded_at": "2026-01-02T02:00:00+00:00"}
        self.assertEqual([last, first], recent_attempts([{"history": [first, last]}]))

    def test_flexible_schedule_chooses_least_loaded_earliest_day(self):
        progress = {
            "a": {"next_review": "2026-01-07"},
            "b": {"next_review": "2026-01-08"},
        }
        self.assertEqual(
            date(2026, 1, 9),
            choose_review_date(2, date(2026, 1, 1), progress),
        )

    def test_legacy_history_is_migrated_and_empty_mastered_is_unverified(self):
        entry = {
            "status": "mastered",
            "mastered_date": "2026-01-01",
            "history": [],
        }
        self.assertTrue(_migrate_entry(entry, date(2026, 1, 2)))
        self.assertFalse(entry["verified"])
        self.assertIsNone(entry["last_rating"])

        old = {
            "status": "review",
            "stage": 0,
            "next_review": "2026-01-03",
            "history": [{"date": "2026-01-01", "result": "helped", "stage": 0}],
        }
        _migrate_entry(old, date(2026, 1, 2))
        self.assertEqual("again", old["history"][0]["rating"])
        self.assertFalse(old["verified"])

if __name__ == "__main__":
    unittest.main()
