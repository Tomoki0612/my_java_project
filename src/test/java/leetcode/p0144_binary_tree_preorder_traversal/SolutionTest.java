package leetcode.p0144_binary_tree_preorder_traversal;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.tree;
import java.util.List;

// Binary Tree Preorder Traversal [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(List.of(1, 2, 3), solution.preorderTraversal(tree(1, null, 2, 3)));
    }

    @Test
    void example2() {
        assertEquals(
            List.of(1, 2, 4, 5, 6, 7, 3, 8, 9),
            solution.preorderTraversal(tree(1, 2, 3, 4, 5, null, 8, null, null, 6, 7, 9))
        );
    }

    @Test
    void emptyTree() {
        assertEquals(List.of(), solution.preorderTraversal(tree()));
    }
}
