package leetcode.p0349_intersection_of_two_arrays;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Intersection of Two Arrays [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  nums1 = [1,2,2,1], nums2 = [2,2]
        // Output: [2]
        assertArrayEquals(new int[]{2}, solution.intersection(new int[]{1,2,2,1}, new int[]{2,2}));
    }

    @Test
    void example2() {
        // Input:  nums1 = [4,9,5], nums2 = [9,4,9,8,4]
        // Output: [9,4]
        assertArrayEquals(new int[]{9,4}, solution.intersection(new int[]{4,9,5}, new int[]{9,4,9,8,4}));
    }
}
