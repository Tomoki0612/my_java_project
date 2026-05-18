package leetcode.p0226_invert_binary_tree;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Invert Binary Tree [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  root = [4,2,7,1,3,6,9]
        // Output: [4,7,2,9,6,3,1]
        // assertEquals(expected, solution.invertTree(...));
    }

    @Test
    void example2() {
        // Input:  root = [2,1,3]
        // Output: [2,3,1]
        // assertEquals(expected, solution.invertTree(...));
    }

    @Test
    void example3() {
        // Input:  root = []
        // Output: []
        // assertEquals(expected, solution.invertTree(...));
    }
}
