package leetcode.p0263_ugly_number;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Ugly Number [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  n = 6
        // Output: true
        assertEquals(true, solution.isUgly(6));
    }

    @Test
    void example2() {
        // Input:  n = 1
        // Output: true
        assertEquals(true, solution.isUgly(1));
    }

    @Test
    void example3() {
        // Input:  n = 14
        // Output: false
        assertEquals(false, solution.isUgly(14));
    }
}
