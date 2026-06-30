package leetcode.p0141_linked_list_cycle;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.listWithCycle;

// Linked List Cycle [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertTrue(solution.hasCycle(listWithCycle(new int[]{3, 2, 0, -4}, 1)));
    }

    @Test
    void example2() {
        assertTrue(solution.hasCycle(listWithCycle(new int[]{1, 2}, 0)));
    }

    @Test
    void example3() {
        assertFalse(solution.hasCycle(listWithCycle(new int[]{1}, -1)));
    }
}
