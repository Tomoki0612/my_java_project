package leetcode.p0268_missing_number;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Missing Number [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(2, solution.missingNumber(new int[]{3, 0, 1}));
    }

    @Test
    void example2() {
        assertEquals(2, solution.missingNumber(new int[]{0, 1}));
    }

    @Test
    void example3() {
        assertEquals(8, solution.missingNumber(new int[]{9, 6, 4, 2, 3, 5, 7, 0, 1}));
    }

    @Test
    void missingZero() {
        assertEquals(0, solution.missingNumber(new int[]{1}));
    }
}
