/*
 * Longest Nice Substring
 * Difficulty: Easy
 * https://leetcode.com/problems/longest-nice-substring/
 *
 * A string `s` is nice if, for every letter of the alphabet that `s`
 * contains, it appears both in uppercase and lowercase. For example,
 * `"abABB"` is nice because `'A'` and `'a'` appear, and `'B'` and `'b'`
 * appear. However, `"abA"` is not because `'b'` appears, but `'B'` does not.
 *
 * Given a string `s`, return the longest substring of `s` that is nice. If
 * there are multiple, return the substring of the earliest occurrence. If
 * there are none, return an empty string.
 *
 *
 *
 * Example 1:
 *
 * Input: s = "YazaAay"
 * Output: "aAa"
 * Explanation: "aAa" is a nice string because 'A/a' is the only letter of the
 * alphabet in s, and both 'A' and 'a' appear.
 * "aAa" is the longest nice substring.
 *
 * Example 2:
 *
 * Input: s = "Bb"
 * Output: "Bb"
 * Explanation: "Bb" is a nice string because both 'B' and 'b' appear. The
 * whole string is a substring.
 *
 * Example 3:
 *
 * Input: s = "c"
 * Output: ""
 * Explanation: There are no nice substrings.
 *
 *
 *
 * Constraints:
 *
 * 	  - `1 <= s.length <= 100`
 *
 * 	  - `s` consists of uppercase and lowercase English letters.
 */
package leetcode.p1763_longest_nice_substring;

import java.util.*;
/**
 * InnerSolution
 */
public interface InnerSolution {


};

class Solution {
    public String longestNiceSubstring(String s) {
        String ans = "";
        for (int i = 0; i < s.length() - 1; i++) {
            Set<Character> set = new HashSet<>();
            for (int j = i; j < s.length(); j++) {
                boolean nice = true;
                set.add(s.charAt(j));
                for (Character c : set) {
                    if (!set.contains(Character.toUpperCase(c)) || !set.contains(Character.toLowerCase(c))) {
                        nice = false;
                    }
                }
                if (nice == true && (j - i + 1) > ans.length()) {
                    ans = s.substring(i, j + 1);
                }
            }
        }
        return ans;
    }
}
