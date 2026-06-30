package leetcode.p0222_count_complete_tree_nodes;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.tree;

// Count Complete Tree Nodes [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(6, solution.countNodes(tree(1, 2, 3, 4, 5, 6)));
    }

    @Test
    void example2() {
        assertEquals(0, solution.countNodes(tree()));
    }

    @Test
    void example3() {
        assertEquals(1, solution.countNodes(tree(1)));
    }
}
