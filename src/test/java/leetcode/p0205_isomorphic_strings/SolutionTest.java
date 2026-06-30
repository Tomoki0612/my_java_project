package leetcode.p0205_isomorphic_strings;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Isomorphic Strings [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertTrue(solution.isIsomorphic("egg", "add"));
    }

    @Test
    void example2() {
        assertFalse(solution.isIsomorphic("foo", "bar"));
    }

    @Test
    void example3() {
        assertTrue(solution.isIsomorphic("paper", "title"));
    }

    @Test
    void rejectsManyToOneMapping() {
        assertFalse(solution.isIsomorphic("badc", "baba"));
    }
}
