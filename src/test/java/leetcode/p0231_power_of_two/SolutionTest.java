package leetcode.p0231_power_of_two;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Power of Two [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  n = 1
        // Output: true
        assertEquals(true, solution.isPowerOfTwo(1));
    }

    @Test
    void example2() {
        // Input:  n = 16
        // Output: true
        assertEquals(true, solution.isPowerOfTwo(16));
    }

    @Test
    void example3() {
        // Input:  n = 3
        // Output: false
        assertEquals(false, solution.isPowerOfTwo(3));
    }
}
