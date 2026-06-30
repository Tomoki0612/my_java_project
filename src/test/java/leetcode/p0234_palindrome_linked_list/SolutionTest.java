package leetcode.p0234_palindrome_linked_list;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import static leetcode.common.TestNodes.list;

// Palindrome Linked List [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertTrue(solution.isPalindrome(list(1, 2, 2, 1)));
    }

    @Test
    void example2() {
        assertFalse(solution.isPalindrome(list(1, 2)));
    }

    @Test
    void oddLengthPalindrome() {
        assertTrue(solution.isPalindrome(list(1, 2, 3, 2, 1)));
    }
}
