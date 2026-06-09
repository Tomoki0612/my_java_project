package leetcode.p0258_add_digits;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Add Digits [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  num = 38
        // Output: 2
        assertEquals(2, solution.addDigits(38));
    }

    @Test
    void example2() {
        // Input:  num = 0
        // Output: 0
        assertEquals(0, solution.addDigits(0));
    }
}
