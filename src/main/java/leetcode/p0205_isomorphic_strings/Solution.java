/*
 * Isomorphic Strings
 * Difficulty: Easy
 * https://leetcode.com/problems/isomorphic-strings/
 *
 * 2つの文字列 `s` と `t` が与えられたとき、
 * それらが同型 (isomorphic) であるかを判定してください。
 *
 * 2つの文字列 `s` と `t` が同型であるとは、
 * `s` の中の文字を置き換えることで `t` を得られることをいいます。
 *
 * ある文字のすべての出現箇所は、文字の順序を保ったまま
 * 別の文字に置き換える必要があります。
 * 2つの異なる文字が同じ文字に対応してはいけませんが、
 * 文字が自分自身に対応することは可能です。
 *
 *
 *
 * Example 1:
 *
 * Input: s = "egg", t = "add"
 *
 * Output: true
 *
 * Explanation:
 *
 * 文字列 `s` と `t` は次のようにして同一にできます：
 *
 * 	  - `'e'` を `'a'` に対応させる。
 *
 * 	  - `'g'` を `'d'` に対応させる。
 *
 * Example 2:
 *
 * Input: s = "f11", t = "b23"
 *
 * Output: false
 *
 * Explanation:
 *
 * `'1'` を `'2'` と `'3'` の両方に対応させる必要があるため、
 * 文字列 `s` と `t` を同一にすることはできません。
 *
 * Example 3:
 *
 * Input: s = "paper", t = "title"
 *
 * Output: true
 *
 *
 *
 * Constraints:
 *
 * 	  - `1 <= s.length <= 5 * 104`
 *
 * 	  - `t.length == s.length`
 *
 * 	  - `s` と `t` は任意の有効な ASCII 文字で構成されます。
 */
package leetcode.p0205_isomorphic_strings;

import java.util.HashMap;
import java.util.Map;

class Solution {
    public boolean isIsomorphic(String s, String t) {
        Map<Character, Character> map = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            if (map.containsKey(s.charAt(i))) {
                if (map.get(s.charAt(i)) != t.charAt(i)) {
                    return false;
                }
            } else {
                if (map.containsValue(t.charAt(i))) {
                    return false;
                }
                map.put(s.charAt(i), t.charAt(i));
            }
        }
        return true;
    }
}
