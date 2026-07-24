import unittest
from unittest.mock import Mock, call, patch

from scripts.done import auto_commit_and_push, collect_rating, parse_args
from scripts.next_action import pick_next


class DoneCliTest(unittest.TestCase):
    def test_non_interactive_rating(self):
        args = parse_args(["203", "--rating", "good"])
        self.assertEqual("good", collect_rating(args))

    @patch("scripts.done.run_git")
    def test_auto_commit_and_push_only_targets_solution_and_progress(self, run_git):
        run_git.side_effect = [
            _git_result(),
            _git_result(),
            _git_result("src/main/java/leetcode/p0203_remove_linked_list_elements/Solution.java\n"
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
