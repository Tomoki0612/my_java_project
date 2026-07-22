package leetcode.p0290_word_pattern;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Word Pattern [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertTrue(solution.wordPattern("abba", "dog cat cat dog"));
    }

    @Test
    void example2() {
        assertFalse(solution.wordPattern("abba", "dog cat cat fish"));
    }

    @Test
    void example3() {
        assertFalse(solution.wordPattern("aaaa", "dog cat cat dog"));
    }
}
