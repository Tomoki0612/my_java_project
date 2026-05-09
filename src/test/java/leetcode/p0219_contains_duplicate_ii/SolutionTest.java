package leetcode.p0219_contains_duplicate_ii;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Contains Duplicate II [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  nums = [1,2,3,1], k = 3
        // Output: true
        assertEquals(true, solution.containsNearbyDuplicate(new int[]{1,2,3,1}, 3));
    }

    @Test
    void example2() {
        // Input:  nums = [1,0,1,1], k = 1
        // Output: true
        assertEquals(true, solution.containsNearbyDuplicate(new int[]{1,0,1,1}, 1));
    }

    @Test
    void example3() {
        // Input:  nums = [1,2,3,1,2,3], k = 2
        // Output: false
        assertEquals(false, solution.containsNearbyDuplicate(new int[]{1,2,3,1,2,3}, 2));
    }
}
