package leetcode.p1763_longest_nice_substring;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Longest Nice Substring [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  s = &quot;YazaAay&quot;
        // Output: &quot;aAa&quot;
        assertEquals(&quot;aAa&quot;, solution.longestNiceSubstring("YazaAay"));
    }

    @Test
    void example2() {
        // Input:  s = &quot;Bb&quot;
        // Output: &quot;Bb&quot;
        assertEquals(&quot;Bb&quot;, solution.longestNiceSubstring("Bb"));
    }

    @Test
    void example3() {
        // Input:  s = &quot;c&quot;
        // Output: &quot;&quot;
        assertEquals(&quot;&quot;, solution.longestNiceSubstring("c"));
    }
}
