package leetcode.p0278_first_bad_version;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// First Bad Version [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  n = 5, bad = 4
        // Output: 4
        solution.bad = 4;  // inject into VersionControl stub (same-package protected field)
        assertEquals(4, solution.firstBadVersion(5));
    }

    @Test
    void example2() {
        // Input:  n = 1, bad = 1
        // Output: 1
        solution.bad = 1;
        assertEquals(1, solution.firstBadVersion(1));
    }
}
