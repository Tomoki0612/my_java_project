"""一時的なローカルGitリポジトリで、同期失敗と復旧を検証する。"""
import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

from scripts import done, sync


class LearningSyncTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.remote = self.root / "remote.git"
        self.git("init", "--bare", str(self.remote))
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Learning Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", ".git/hooks")
        self.key = "p0203_remove_linked_list_elements"
        self.src = self.repo / "src/main/java/leetcode"
        self.progress_path = self.src / "progress.json"
        self.solution = self.src / self.key / "Solution.java"
        paths = [
            self.solution,
            self.repo / "src/test/java/leetcode" / self.key / "SolutionTest.java",
            self.repo / "scripts/placeholder.py",
            *[self.repo / name for name in ("README.md", "CLAUDE.md", "Makefile", "pom.xml", ".github/workflows/test.yml")],
        ]
        for path in paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("initial\n")
        self.save_progress({self.key: {
            "title": "Remove Linked List Elements", "difficulty": "Easy",
            "status": "in_progress", "stage": None, "history": [], "retries": 0,
        }})
        self.git("add", ".")
        self.git("commit", "-m", "initial")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        for mock in (
            patch.multiple(done, PROJECT_ROOT=str(self.repo), SRC_ROOT=str(self.src), PROGRESS_FILE=str(self.progress_path)),
            patch.object(done, "load_progress", side_effect=lambda: (self.read_progress(), False)),
            patch.object(done, "save_progress", side_effect=self.save_progress),
            patch.object(sync, "PROJECT_ROOT", str(self.repo)),
        ):
            mock.start()
            self.addCleanup(mock.stop)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, capture_output=True, text=True).stdout.strip()

    def read_progress(self):
        return json.loads(self.progress_path.read_text())

    def save_progress(self, progress):
        self.progress_path.write_text(json.dumps(progress))

    def reject_push(self):
        hook = self.remote / "hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        return hook

    def call_done(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = done.main(["203", *args])
        return result, output.getvalue()

    def call_sync(self, *args):
        original_run = sync.run
        # 期待どおりに失敗するGitコマンドの出力もテスト内に収める。
        def capture_run(command, check=False, capture=False):
            return original_run(command, check=check, capture=True)

        with contextlib.redirect_stdout(io.StringIO()) as output, patch.object(sync, "run", side_effect=capture_run):
            result = sync.main(list(args))
        return result, output.getvalue()

    def remote_head(self):
        return self.git("--git-dir", str(self.remote), "rev-parse", "refs/heads/main")

    def test_done_retry_after_push_failure_preserves_evaluation_and_commit(self):
        hook = self.reject_push()
        self.solution.write_text("solved\n")
        result, output = self.call_done("--rating", "good", "--no-test")
        self.assertEqual(1, result)
        self.assertIn("--sync-only", output)
        saved = self.progress_path.read_bytes()
        head = self.git("rev-parse", "HEAD")
        entry = self.read_progress()[self.key]
        self.assertEqual(1, entry["stage"])
        self.assertEqual(1, len(entry["history"]))
        self.assertNotEqual(head, self.remote_head())
        hook.unlink()
        with patch("builtins.input", side_effect=AssertionError("retry must not prompt")), patch.object(
            done, "run_tests", side_effect=AssertionError("retry must not run tests")
        ):
            self.assertEqual(0, self.call_done()[0])
        self.assertEqual(saved, self.progress_path.read_bytes())
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(head, self.remote_head())

    def test_explicit_sync_only_retries_on_a_later_day(self):
        hook = self.reject_push()
        self.assertEqual(1, self.call_done("--rating", "good", "--no-test")[0])
        saved = self.progress_path.read_bytes()
        hook.unlink()
        with patch.object(done, "date") as clock, patch("builtins.input", side_effect=AssertionError):
            clock.today.return_value = date.today() + timedelta(days=1)
            self.assertEqual(0, self.call_done("--sync-only")[0])
        self.assertEqual(saved, self.progress_path.read_bytes())
        self.assertEqual(self.git("rev-parse", "HEAD"), self.remote_head())

    def test_commit_failure_can_be_retried_without_another_evaluation(self):
        hook = self.repo / ".git/hooks/pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        self.assertEqual(1, self.call_done("--rating", "good", "--no-test")[0])
        self.assertEqual("", self.git("diff", "--cached", "--name-only"))
        saved = self.progress_path.read_bytes()
        hook.unlink()
        self.assertEqual(0, self.call_done()[0])
        self.assertEqual(saved, self.progress_path.read_bytes())
        self.assertEqual(self.git("rev-parse", "HEAD"), self.remote_head())

    def test_again_retry_does_not_reset_solution_or_increment_retries_twice(self):
        hook = self.reject_push()
        with patch.object(done, "reset_solution") as reset:
            self.assertEqual(1, self.call_done("--rating", "again")[0])
            hook.unlink()
            self.assertEqual(0, self.call_done()[0])
        reset.assert_called_once_with(self.key)
        entry = self.read_progress()[self.key]
        self.assertEqual(1, entry["retries"])
        self.assertEqual(1, len(entry["history"]))

    def test_same_day_repeat_requires_explicit_new_attempt(self):
        self.assertEqual(0, self.call_done("--rating", "good", "--no-test")[0])
        self.assertEqual(0, self.call_done("--rating", "easy", "--no-test")[0])
        self.assertEqual(1, len(self.read_progress()[self.key]["history"]))
        self.assertEqual(0, self.call_done("--new-attempt", "--rating", "easy", "--no-test")[0])
        entry = self.read_progress()[self.key]
        self.assertEqual(["good", "easy"], [attempt["rating"] for attempt in entry["history"]])
        self.assertEqual(3, entry["stage"])

    def test_sync_pushes_existing_commit_without_changing_progress(self):
        hook = self.reject_push()
        self.assertEqual(1, self.call_done("--rating", "good", "--no-test")[0])
        saved = self.progress_path.read_bytes()
        head = self.git("rev-parse", "HEAD")
        hook.unlink()
        with patch("builtins.input", return_value="n"):
            self.assertEqual(1, self.call_sync()[0])
        self.assertNotEqual(head, self.remote_head())
        self.assertEqual(0, self.call_sync("--yes")[0])
        self.assertEqual(head, self.remote_head())
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(saved, self.progress_path.read_bytes())

    def test_sync_rebases_unpushed_evaluation_onto_remote_changes(self):
        other = self.root / "other"
        self.git("clone", "--branch", "main", str(self.remote), str(other))
        self.git("-C", str(other), "config", "user.name", "Other Test")
        self.git("-C", str(other), "config", "user.email", "other@example.invalid")
        self.git("-C", str(other), "config", "commit.gpgsign", "false")
        self.git("-C", str(other), "config", "core.hooksPath", ".git/hooks")
        (other / "remote-only.txt").write_text("remote change\n")
        self.git("-C", str(other), "add", "remote-only.txt")
        self.git("-C", str(other), "commit", "-m", "remote change")
        self.git("-C", str(other), "push")
        remote_commit = self.remote_head()

        self.assertEqual(1, self.call_done("--rating", "good", "--no-test")[0])
        saved = self.progress_path.read_bytes()
        self.assertEqual(0, self.call_sync("--yes")[0])
        self.assertEqual(saved, self.progress_path.read_bytes())
        self.assertEqual("remote change\n", (self.repo / "remote-only.txt").read_text())
        self.assertEqual(self.git("rev-parse", "HEAD"), self.remote_head())
        self.assertEqual(remote_commit, self.git("rev-parse", "HEAD^"))
        self.assertEqual(1, len(self.read_progress()[self.key]["history"]))

    def test_sync_push_failure_is_recoverable_with_no_new_changes(self):
        hook = self.reject_push()
        (self.repo / "README.md").write_text("updated\n")
        self.assertEqual(1, self.call_sync("--yes")[0])
        head = self.git("rev-parse", "HEAD")
        self.assertEqual("", self.git("status", "--porcelain"))
        hook.unlink()
        self.assertEqual(0, self.call_sync("--yes")[0])
        self.assertEqual(head, self.remote_head())

    def test_existing_staged_changes_are_not_committed_by_retry(self):
        self.assertEqual(0, self.call_done("--rating", "good", "--no-test")[0])
        unrelated = self.repo / "private.txt"
        unrelated.write_text("keep separate\n")
        self.git("add", "private.txt")
        head = self.git("rev-parse", "HEAD")
        saved = self.progress_path.read_bytes()
        self.assertEqual(1, self.call_done("--sync-only")[0])
        self.assertEqual(1, self.call_sync("--yes")[0])
        self.assertEqual("private.txt", self.git("diff", "--cached", "--name-only"))
        self.assertEqual(head, self.git("rev-parse", "HEAD"))
        self.assertEqual(saved, self.progress_path.read_bytes())

    def test_sync_cancellation_preserves_changes_and_cleans_its_staging(self):
        (self.repo / "README.md").write_text("updated\n")
        head = self.git("rev-parse", "HEAD")
        for answer in ("n", EOFError(), KeyboardInterrupt()):
            with self.subTest(answer=type(answer).__name__):
                kwargs = {"return_value": answer} if isinstance(answer, str) else {"side_effect": answer}
                with patch("builtins.input", **kwargs):
                    self.assertEqual(1, self.call_sync()[0])
                self.assertEqual("", self.git("diff", "--cached", "--name-only"))
                self.assertEqual("updated\n", (self.repo / "README.md").read_text())
                self.assertEqual(head, self.git("rev-parse", "HEAD"))

    def test_sync_only_without_a_record_does_not_commit(self):
        head = self.git("rev-parse", "HEAD")
        self.assertEqual(1, self.call_done("--sync-only")[0])
        self.assertEqual(head, self.git("rev-parse", "HEAD"))


if __name__ == "__main__":
    unittest.main()
