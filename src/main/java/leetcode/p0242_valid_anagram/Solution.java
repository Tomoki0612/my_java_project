/*
 * Valid Anagram
 * Difficulty: Easy
 * https://leetcode.com/problems/valid-anagram/
 *
 * 2つの文字列 `s` と `t` が与えられたとき、
 * `t` が `s` のアナグラムであれば `true` を、
 * そうでなければ `false` を返してください。
 *
 *
 *
 * Example 1:
 *
 * Input: s = "anagram", t = "nagaram"
 *
 * Output: true
 *
 * Example 2:
 *
 * Input: s = "rat", t = "car"
 *
 * Output: false
 *
 *
 *
 * Constraints:
 *
 * 	  - `1 <= s.length, t.length <= 5 * 104`
 *
 * 	  - `s` と `t` は英小文字のみで構成されます。
 *
 *
 *
 * Follow up: 入力にUnicode文字が含まれる場合はどうしますか？
 * そのような場合に対応するために、解法をどう変更しますか？
 */
package leetcode.p0242_valid_anagram;

import java.util.*;

class Solution {
    public boolean isAnagram(String s, String t) {
        
        List<Character> list = new ArrayList<>();
        for (int i = 0; i < s.length(); i++) {
            list.add(s.charAt(i));
        }

        for (int i = 0; i < t.length(); i++) {
            if (list.contains(t.charAt(i))) {
                list.remove(list.indexOf(t.charAt(i)));
            } else return false;
        }
        return list.size() == 0;
    }
}
