package leetcode.p0228_summary_ranges;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

// Summary Ranges [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertEquals(List.of("0->2", "4->5", "7"), solution.summaryRanges(new int[]{0, 1, 2, 4, 5, 7}));
    }

    @Test
    void example2() {
        assertEquals(List.of("0", "2->4", "6", "8->9"), solution.summaryRanges(new int[]{0, 2, 3, 4, 6, 8, 9}));
    }

    @Test
    void emptyInput() {
        assertEquals(List.of(), solution.summaryRanges(new int[]{}));
    }
}
