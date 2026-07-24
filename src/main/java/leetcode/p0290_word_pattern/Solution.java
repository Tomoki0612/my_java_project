/*
 * Word Pattern
 * Difficulty: Easy
 * https://leetcode.com/problems/word-pattern/
 *
 * Given a `pattern` and a string `s`, find if `s` follows the same pattern.
 *
 * Here follow means a full match, such that there is a bijection between a
 * letter in `pattern` and a non-empty word in `s`. Specifically:
 *
 * 	  - Each letter in `pattern` maps to exactly one unique word in `s`.
 *
 * 	  - Each unique word in `s` maps to exactly one letter in `pattern`.
 *
 * 	  - No two letters map to the same word, and no two words map to the same
 * letter.
 *
 *
 *
 * Example 1:
 *
 * Input: pattern = "abba", s = "dog cat cat dog"
 *
 * Output: true
 *
 * Explanation:
 *
 * The bijection can be established as:
 *
 * 	  - `'a'` maps to `"dog"`.
 *
 * 	  - `'b'` maps to `"cat"`.
 *
 * Example 2:
 *
 * Input: pattern = "abba", s = "dog cat cat fish"
 *
 * Output: false
 *
 * Example 3:
 *
 * Input: pattern = "aaaa", s = "dog cat cat dog"
 *
 * Output: false
 *
 *
 *
 * Constraints:
 *
 * 	  - `1 <= pattern.length <= 300`
 *
 * 	  - `pattern` contains only lower-case English letters.
 *
 * 	  - `1 <= s.length <= 3000`
 *
 * 	  - `s` contains only lowercase English letters and spaces `' '`.
 *
 * 	  - `s` does not contain any leading or trailing spaces.
 *
 * 	  - All the words in `s` are separated by a single space.
 */
package leetcode.p0290_word_pattern;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    public boolean wordPattern(String pattern, String s) {
        List<String> list = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == ' ') {
                list.add(sb.toString());
                sb = new StringBuilder();
            } else {
                sb.append(s.charAt(i));
            }
        }

        list.add(sb.toString());

        if (list.size() != pattern.length()) {
            return false;
        }

        Map<Character, String> map = new HashMap<>();
        for (int i = 0; i < pattern.length(); i++) {
            if (map.containsKey(pattern.charAt(i))) {
                if (!map.get(pattern.charAt(i)).equals(list.get(i))) {
                    return false;
                }
            } else {
                if (map.containsValue(list.get(i))) {
                    return false;
                } else {
                    map.put(pattern.charAt(i), list.get(i));
                }
            }
        }
        return true;
    }
}
