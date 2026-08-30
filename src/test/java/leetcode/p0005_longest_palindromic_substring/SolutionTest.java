package leetcode.p0005_longest_palindromic_substring;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

// Longest Palindromic Substring [Medium]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  s = "babad"
        // Output: "bab"
        assertEquals("bab", solution.longestPalindrome("babad"));
    }

    @Test
    void example2() {
        // Input:  s = "cbbd"
        // Output: "bb"
        assertEquals("bb", solution.longestPalindrome("cbbd"));
    }

    @Test
    void example3() {
        // Input:  s = "abbcccba"
        // Output: "bcccb"
        assertEquals("bcccb", solution.longestPalindrome("abbcccba"));
    }
}
