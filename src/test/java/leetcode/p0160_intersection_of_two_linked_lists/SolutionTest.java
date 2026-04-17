package leetcode.p0160_intersection_of_two_linked_lists;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Intersection of Two Linked Lists [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA = 2, skipB = 3
        // Output: Intersected at &#39;8&#39;
        // assertEquals(expected, solution.getIntersectionNode(...));
    }

    @Test
    void example2() {
        // Input:  intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3, skipB = 1
        // Output: Intersected at &#39;2&#39;
        // assertEquals(expected, solution.getIntersectionNode(...));
    }

    @Test
    void example3() {
        // Input:  intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB = 2
        // Output: No intersection
        // assertEquals(expected, solution.getIntersectionNode(...));
    }
}
