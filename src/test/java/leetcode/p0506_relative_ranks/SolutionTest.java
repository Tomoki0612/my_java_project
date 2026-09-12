package leetcode.p0506_relative_ranks;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Relative Ranks [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  score = [5,4,3,2,1]
        // Output: ["Gold Medal","Silver Medal","Bronze Medal","4","5"]
        assertArrayEquals(new String[]{"Gold Medal","Silver Medal","Bronze Medal","4","5"}, solution.findRelativeRanks(new int[]{5,4,3,2,1}));
    }

    @Test
    void example2() {
        // Input:  score = [10,3,8,9,4]
        // Output: ["Gold Medal","5","Bronze Medal","Silver Medal","4"]
        assertArrayEquals(new String[]{"Gold Medal","5","Bronze Medal","Silver Medal","4"}, solution.findRelativeRanks(new int[]{10,3,8,9,4}));
    }
}
