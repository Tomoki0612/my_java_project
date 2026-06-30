package leetcode.p0257_binary_tree_paths;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.tree;
import java.util.List;

// Binary Tree Paths [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(List.of("1->2->5", "1->3"), solution.binaryTreePaths(tree(1, 2, 3, null, 5)));
    }

    @Test
    void example2() {
        assertEquals(List.of("1"), solution.binaryTreePaths(tree(1)));
    }
}
