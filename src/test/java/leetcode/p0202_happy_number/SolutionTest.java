package leetcode.p0202_happy_number;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Happy Number [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  n = 19
        // Output: true
        assertEquals(true, solution.isHappy(19));
    }

    @Test
    void example2() {
        // Input:  n = 2
        // Output: false
        assertEquals(false, solution.isHappy(2));
    }
}
