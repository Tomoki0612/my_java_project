package leetcode.p0203_remove_linked_list_elements;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.list;
import static leetcode.common.TestNodes.toArray;

// Remove Linked List Elements [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertArrayEquals(
            new int[]{1, 2, 3, 4, 5},
            toArray(solution.removeElements(list(1, 2, 6, 3, 4, 5, 6), 6))
        );
    }

    @Test
    void example2() {
        assertArrayEquals(new int[]{}, toArray(solution.removeElements(list(), 1)));
    }

    @Test
    void example3() {
        assertArrayEquals(new int[]{}, toArray(solution.removeElements(list(7, 7, 7, 7), 7)));
    }
}
