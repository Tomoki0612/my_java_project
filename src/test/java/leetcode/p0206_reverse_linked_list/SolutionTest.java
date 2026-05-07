package leetcode.p0206_reverse_linked_list;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Reverse Linked List [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  head = [1,2,3,4,5]
        // Output: [5,4,3,2,1]
        // assertEquals(expected, solution.reverseList(...));
    }

    @Test
    void example2() {
        // Input:  head = [1,2]
        // Output: [2,1]
        // assertEquals(expected, solution.reverseList(...));
    }

    @Test
    void example3() {
        // Input:  head = []
        // Output: []
        // assertEquals(expected, solution.reverseList(...));
    }
}
