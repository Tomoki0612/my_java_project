package leetcode.p0203_remove_linked_list_elements;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Remove Linked List Elements [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  head = [1,2,6,3,4,5,6], val = 6
        // Output: [1,2,3,4,5]
        // assertEquals(expected, solution.removeElements(...));
    }

    @Test
    void example2() {
        // Input:  head = [], val = 1
        // Output: []
        // assertEquals(expected, solution.removeElements(...));
    }

    @Test
    void example3() {
        // Input:  head = [7,7,7,7], val = 7
        // Output: []
        // assertEquals(expected, solution.removeElements(...));
    }
}
