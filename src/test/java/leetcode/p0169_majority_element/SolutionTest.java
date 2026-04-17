package leetcode.p0169_majority_element;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Majority Element [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  nums = [3,2,3]
        // Output: 3
        assertEquals(3, solution.majorityElement(new int[]{3,2,3}));
    }

    @Test
    void example2() {
        // Input:  nums = [2,2,1,1,1,2,2]
        // Output: 2
        assertEquals(2, solution.majorityElement(new int[]{2,2,1,1,1,2,2}));
    }
}
