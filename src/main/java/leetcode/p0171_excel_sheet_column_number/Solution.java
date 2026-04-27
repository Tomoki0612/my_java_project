/*
 * Excel Sheet Column Number
 * Difficulty: Easy
 * https://leetcode.com/problems/excel-sheet-column-number/
 *
 * Excelシートに表示される列タイトルを表す文字列 `columnTitle` が与えられたとき、
 * それに対応する列番号を返してください。
 *
 * 例:
 *
 * A -> 1
 * B -> 2
 * C -> 3
 * ...
 * Z -> 26
 * AA -> 27
 * AB -> 28
 * ...
 *
 *
 *
 * Example 1:
 *
 * Input: columnTitle = "A"
 * Output: 1
 *
 * Example 2:
 *
 * Input: columnTitle = "AB"
 * Output: 28
 *
 * Example 3:
 *
 * Input: columnTitle = "ZY"
 * Output: 701
 *
 *
 *
 * 制約:
 *
 * 	  - `1 <= columnTitle.length <= 7`
 *
 * 	  - `columnTitle` は大文字の英字のみで構成される。
 *
 * 	  - `columnTitle` は `["A", "FXSHRXW"]` の範囲内である。
 */
package leetcode.p0171_excel_sheet_column_number;

class Solution {
    public int titleToNumber(String columnTitle) {
        int sum = 0;
        for (int i = 0; i < columnTitle.length(); i++) {
            sum += (columnTitle.charAt(i) - 64) * (int)Math.pow(26, columnTitle.length() - 1 - i);
        }
        return sum;
    }
}
