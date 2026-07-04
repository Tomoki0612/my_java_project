package leetcode.p0350_intersection_of_two_arrays_ii;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Intersection of Two Arrays II [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  nums1 = [1,2,2,1], nums2 = [2,2]
        // Output: [2,2]
        assertArrayEquals(new int[]{2,2}, solution.intersect(new int[]{1,2,2,1}, new int[]{2,2}));
    }

    @Test
    void example2() {
        // Input:  nums1 = [4,9,5], nums2 = [9,4,9,8,4]
        // Output: [4,9]
        assertArrayEquals(new int[]{4,9}, solution.intersect(new int[]{4,9,5}, new int[]{9,4,9,8,4}));
    }
}
