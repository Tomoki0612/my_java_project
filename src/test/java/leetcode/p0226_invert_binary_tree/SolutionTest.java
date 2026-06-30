package leetcode.p0226_invert_binary_tree;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.toLevelOrder;
import static leetcode.common.TestNodes.tree;
import java.util.List;

// Invert Binary Tree [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(
            List.of(4, 7, 2, 9, 6, 3, 1),
            toLevelOrder(solution.invertTree(tree(4, 2, 7, 1, 3, 6, 9)))
        );
    }

    @Test
    void example2() {
        assertEquals(List.of(2, 3, 1), toLevelOrder(solution.invertTree(tree(2, 1, 3))));
    }

    @Test
    void example3() {
        assertEquals(List.of(), toLevelOrder(solution.invertTree(tree())));
    }
}
