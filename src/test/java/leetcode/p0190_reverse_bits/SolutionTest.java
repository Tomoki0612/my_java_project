package leetcode.p0190_reverse_bits;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Reverse Bits [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(964176192, solution.reverseBits(43261596));
    }

    @Test
    void example2() {
        assertEquals(1073741822, solution.reverseBits(2147483644));
    }

    @Test
    void zero() {
        assertEquals(0, solution.reverseBits(0));
    }
}
