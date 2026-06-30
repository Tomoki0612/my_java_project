package leetcode.p0206_reverse_linked_list;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.list;
import static leetcode.common.TestNodes.toArray;

// Reverse Linked List [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertArrayEquals(new int[]{5, 4, 3, 2, 1}, toArray(solution.reverseList(list(1, 2, 3, 4, 5))));
    }

    @Test
    void example2() {
        assertArrayEquals(new int[]{2, 1}, toArray(solution.reverseList(list(1, 2))));
    }

    @Test
    void example3() {
        assertArrayEquals(new int[]{}, toArray(solution.reverseList(list())));
    }
}
