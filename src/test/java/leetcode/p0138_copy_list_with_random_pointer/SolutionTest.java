package leetcode.p0138_copy_list_with_random_pointer;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Copy List with Random Pointer [Medium]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
        // Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
        // assertEquals(expected, solution.copyRandomList(...));
    }

    @Test
    void example2() {
        // Input:  head = [[1,1],[2,1]]
        // Output: [[1,1],[2,1]]
        // assertEquals(expected, solution.copyRandomList(...));
    }

    @Test
    void example3() {
        // Input:  head = [[3,null],[3,0],[3,null]]
        // Output: [[3,null],[3,0],[3,null]]
        // assertEquals(expected, solution.copyRandomList(...));
    }
}
