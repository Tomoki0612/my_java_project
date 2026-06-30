package leetcode.p0242_valid_anagram;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Valid Anagram [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertTrue(solution.isAnagram("anagram", "nagaram"));
    }

    @Test
    void example2() {
        assertFalse(solution.isAnagram("rat", "car"));
    }

    @Test
    void differentLengths() {
        assertFalse(solution.isAnagram("a", "ab"));
    }
}
