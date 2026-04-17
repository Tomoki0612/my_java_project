/*
 * Linked List Cycle
 * Difficulty: Easy
 * https://leetcode.com/problems/linked-list-cycle/
 *
 * `head`（連結リストの先頭）が与えられるので、
 * その連結リストにサイクルが存在するかどうかを判定してください。
 *
 * `next` ポインタをたどり続けることで、
 * 再び同じノードに到達できるノードが存在する場合、
 * 連結リストにはサイクルがあります。
 * 内部的に、`pos` はテールの `next` ポインタが接続している
 * ノードのインデックスを示します。
 * なお、`pos` は引数として渡されません。
 *
 * 連結リストにサイクルがあれば `true` を、
 * なければ `false` を返してください。
 *
 * Example 1:
 *
 * Input: head = [3,2,0,-4], pos = 1
 * Output: true
 * Explanation: There is a cycle in the linked list, where the tail connects
 * to the 1st node (0-indexed).
 *
 * Example 2:
 *
 * Input: head = [1,2], pos = 0
 * Output: true
 * Explanation: There is a cycle in the linked list, where the tail connects
 * to the 0th node.
 *
 * Example 3:
 *
 * Input: head = [1], pos = -1
 * Output: false
 * Explanation: There is no cycle in the linked list.
 *
 * 制約:
 *
 * - リスト内のノード数は `[0, 104]` の範囲です。
 * - `-105 <= Node.val <= 105`
 * - `pos` は `-1` か、連結リスト内の有効なインデックスです。
 *
 * フォローアップ: `O(1)`（定数）メモリで解くことはできますか？
 */
package leetcode.p0141_linked_list_cycle;
import java.util.ArrayList;
import java.util.List;

import leetcode.common.ListNode;

/**
 * Definition for singly-linked list.
 * class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode cur = head;
        List<ListNode> list = new ArrayList<>();
        while (cur != null) {
            for (int i = 0; i < list.size(); i++) {
                if (list.get(i) == cur) {
                    return true;
                }
            }
            list.add(cur);
            cur = cur.next;
        }
        return false;
    }
}
