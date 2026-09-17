package leetcode.p0392_is_subsequence;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Is Subsequence [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  s = "abc", t = "ahbgdc"
        // Output: true
        assertEquals(true, solution.isSubsequence("abc", "ahbgdc"));
    }

    @Test
    void example2() {
        // Input:  s = "axc", t = "ahbgdc"
        // Output: false
        assertEquals(false, solution.isSubsequence("axc", "ahbgdc"));
    }
}
