package leetcode.p0168_excel_sheet_column_title;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Excel Sheet Column Title [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        // Input:  columnNumber = 1
        // Output: "A"
        assertEquals("A", solution.convertToTitle(1));
    }

    @Test
    void example2() {
        // Input:  columnNumber = 28
        // Output: "AB"
        assertEquals("AB", solution.convertToTitle(28));
    }

    @Test
    void example3() {
        // Input:  columnNumber = 701
        // Output: "ZY"
        assertEquals("ZY", solution.convertToTitle(701));
    }
}
