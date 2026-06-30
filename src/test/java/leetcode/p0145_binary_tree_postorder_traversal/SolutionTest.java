package leetcode.p0145_binary_tree_postorder_traversal;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.tree;
import java.util.List;

// Binary Tree Postorder Traversal [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(List.of(3, 2, 1), solution.postorderTraversal(tree(1, null, 2, 3)));
    }

    @Test
    void example2() {
        assertEquals(
            List.of(4, 6, 7, 5, 2, 9, 8, 3, 1),
            solution.postorderTraversal(tree(1, 2, 3, 4, 5, null, 8, null, null, 6, 7, 9))
        );
    }

    @Test
    void emptyTree() {
        assertEquals(List.of(), solution.postorderTraversal(tree()));
    }
}
