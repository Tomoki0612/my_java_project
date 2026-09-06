import unittest
from unittest.mock import patch

from scripts.recommend_new import pick_candidates, recent_topic_counts, score_candidate


class RecommendationTest(unittest.TestCase):
    def test_recent_topic_limit_uses_latest_time_within_the_day(self):
        progress = {
            "first": {"topic_tags": ["Array"], "history": [{
                "date": "2026-01-02", "recorded_at": "2026-01-02T10:00:00+09:00",
            }]},
            "second": {"topic_tags": ["Hash Table"], "history": [{
                "date": "2026-01-02", "recorded_at": "2026-01-02T11:00:00+09:00",
            }]},
        }
        self.assertEqual({"Hash Map/Set": 1}, recent_topic_counts(progress, limit=1))

    def test_candidate_score_rewards_multiple_weak_patterns(self):
        question = {
            "questionFrontendId": "200",
            "topicTags": [{"name": "Array"}, {"name": "Hash Table"}],
        }
        scored = score_candidate(
            question,
            "Array/String",
            0,
            {"Array/String": 20, "Hash Map/Set": 15},
            {},
        )
        self.assertIn("複数弱点に一致", scored["reasons"])
        self.assertGreater(scored["score"], 35)

    @patch("scripts.recommend_new.fetch_candidates")
    def test_paid_registered_and_duplicate_candidates_are_skipped(self, fetch):
        fetch.return_value = [
            {"questionFrontendId": "1", "isPaidOnly": False},
            {"questionFrontendId": "2", "isPaidOnly": True},
            {"questionFrontendId": "3", "isPaidOnly": False},
            {"questionFrontendId": "4", "isPaidOnly": False},
        ]
        result = pick_candidates("Array", {1}, {3}, per_topic=2, difficulty="easy")
        self.assertEqual([4], [int(item["questionFrontendId"]) for item in result])


if __name__ == "__main__":
    unittest.main()
