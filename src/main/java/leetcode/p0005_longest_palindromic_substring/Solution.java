/*
 * Longest Palindromic Substring
 * Difficulty: Medium
 * https://leetcode.com/problems/longest-palindromic-substring/
 *
 * Given a string `s`, return the longest palindromic substring in `s`.
 *
 *
 *
 * Example 1:
 *
 * Input: s = "babad"
 * Output: "bab"
 * Explanation: "aba" is also a valid answer.
 *
 * Example 2:
 *
 * Input: s = "cbbd"
 * Output: "bb"
 *
 *
 *
 * Constraints:
 *
 * 	  - `1 <= s.length <= 1000`
 *
 * 	  - `s` consist of only digits and English letters.
 */
package leetcode.p0005_longest_palindromic_substring;

class Solution {
    public String longestPalindrome(String s) {
        int maxStart = 0;
        int maxLength = 1;
        for (int i = 0; i < s.length(); i++) {
            int left = i;
            int right = i;
            int length;
            while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
                length = right -left + 1; 
                if (maxLength < length) {
                    maxLength = length;
                    maxStart = left;
                }

                left--;
                right++;
            }

            left = i;
            right = i + 1; 
            while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {
                length = right - left + 1;
                if (maxLength < length) {
                    maxLength = length;
                    maxStart = left;
                }

                left--;
                right++;
            }
        }
        return s.substring(maxStart, maxStart + maxLength);
    }
}
