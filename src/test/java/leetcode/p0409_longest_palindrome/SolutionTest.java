package leetcode.p0409_longest_palindrome;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Longest Palindrome [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  s = "abccccdd"
        // Output: 7
        assertEquals(7, solution.longestPalindrome("abccccdd"));
    }

    @Test
    void example2() {
        // Input:  s = "a"
        // Output: 1
        assertEquals(1, solution.longestPalindrome("a"));
    }
}
