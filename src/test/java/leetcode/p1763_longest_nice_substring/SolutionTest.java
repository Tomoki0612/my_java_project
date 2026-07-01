package leetcode.p1763_longest_nice_substring;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Longest Nice Substring [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  s = "YazaAay"
        // Output: "aAa"
        assertEquals("aAa", solution.longestNiceSubstring("YazaAay"));
    }

    @Test
    void example2() {
        // Input:  s = "Bb"
        // Output: "Bb"
        assertEquals("Bb", solution.longestNiceSubstring("Bb"));
    }

    @Test
    void example3() {
        // Input:  s = "c"
        // Output: ""
        assertEquals("", solution.longestNiceSubstring("c"));
    }
}
