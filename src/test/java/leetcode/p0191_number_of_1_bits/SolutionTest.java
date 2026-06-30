package leetcode.p0191_number_of_1_bits;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Number of 1 Bits [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(3, solution.hammingWeight(11));
    }

    @Test
    void example2() {
        assertEquals(1, solution.hammingWeight(128));
    }

    @Test
    void example3() {
        assertEquals(30, solution.hammingWeight(2147483645));
    }
}
