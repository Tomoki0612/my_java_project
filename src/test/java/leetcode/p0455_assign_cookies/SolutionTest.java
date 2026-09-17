package leetcode.p0455_assign_cookies;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Assign Cookies [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  g = [1,2,3], s = [1,1]
        // Output: 1
        assertEquals(1, solution.findContentChildren(new int[]{1,2,3}, new int[]{1,1}));
    }

    @Test
    void example2() {
        // Input:  g = [1,2], s = [1,2,3]
        // Output: 2
        assertEquals(2, solution.findContentChildren(new int[]{1,2}, new int[]{1,2,3}));
    }
}
