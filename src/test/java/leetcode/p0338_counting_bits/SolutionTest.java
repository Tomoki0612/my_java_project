package leetcode.p0338_counting_bits;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Counting Bits [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  n = 2
        // Output: [0,1,1]
        assertArrayEquals(new int[]{0,1,1}, solution.countBits(2));
    }

    @Test
    void example2() {
        // Input:  n = 5
        // Output: [0,1,1,2,1,2]
        assertArrayEquals(new int[]{0,1,1,2,1,2}, solution.countBits(5));
    }
}
