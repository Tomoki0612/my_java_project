package leetcode.p0141_linked_list_cycle;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Linked List Cycle [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  head = [3,2,0,-4], pos = 1
        // Output: true
        // assertEquals(expected, solution.hasCycle(...));
    }

    @Test
    void example2() {
        // Input:  head = [1,2], pos = 0
        // Output: true
        // assertEquals(expected, solution.hasCycle(...));
    }

    @Test
    void example3() {
        // Input:  head = [1], pos = -1
        // Output: false
        // assertEquals(expected, solution.hasCycle(...));
    }
}
