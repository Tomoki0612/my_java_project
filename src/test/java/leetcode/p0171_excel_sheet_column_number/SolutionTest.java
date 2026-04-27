package leetcode.p0171_excel_sheet_column_number;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Excel Sheet Column Number [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  columnTitle = &quot;A&quot;
        // Output: 1
        assertEquals(1, solution.titleToNumber("A"));
    }

    @Test
    void example2() {
        // Input:  columnTitle = &quot;AB&quot;
        // Output: 28
        assertEquals(28, solution.titleToNumber("AB"));
    }

    @Test
    void example3() {
        // Input:  columnTitle = &quot;ZY&quot;
        // Output: 701
        assertEquals(701, solution.titleToNumber("ZY"));
    }
}
