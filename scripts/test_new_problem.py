#!/usr/bin/env python3

import unittest

from scripts.new_problem import extract_examples


class ExtractExamplesTest(unittest.TestCase):
    def test_extracts_legacy_pre_examples(self):
        content = """
        <pre><strong>Input:</strong> nums = [1,2]
        <strong>Output:</strong> 3
        <strong>Explanation:</strong> example</pre>
        """

        self.assertEqual(
            [{"input": "nums = [1,2]", "output": "3"}],
            extract_examples(content),
        )

    def test_extracts_modern_block_examples(self):
        content = """
        <div class="example-block">
          <p><strong>Example 1:</strong></p>
          <p><strong>Input:</strong> pattern = &quot;abba&quot;, s = &quot;dog cat cat dog&quot;</p>
          <p><strong>Output:</strong> true</p>
          <p><strong>Explanation:</strong> The mapping is valid.</p>
        </div>
        <div class="example-block">
          <p><strong>Example 2:</strong></p>
          <p><strong>Input:</strong> pattern = &quot;abba&quot;, s = &quot;dog cat cat fish&quot;</p>
          <p><strong>Output:</strong> false</p>
        </div>
        <p><strong>Constraints:</strong></p>
        """

        self.assertEqual(
            [
                {
                    "input": 'pattern = "abba", s = "dog cat cat dog"',
                    "output": "true",
                },
                {
                    "input": 'pattern = "abba", s = "dog cat cat fish"',
                    "output": "false",
                },
            ],
            extract_examples(content),
        )


if __name__ == "__main__":
    unittest.main()
