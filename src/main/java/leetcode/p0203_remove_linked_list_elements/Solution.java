/*
 * Remove Linked List Elements
 * Difficulty: Easy
 * https://leetcode.com/problems/remove-linked-list-elements/
 *
 * 連結リストの `head` と整数 `val` が与えられたとき、
 * `Node.val == val` を満たすすべてのノードを連結リストから削除し、
 * 新しい head を返してください。
 *
 *
 *
 * 例 1:
 *
 * 入力: head = [1,2,6,3,4,5,6], val = 6
 * 出力: [1,2,3,4,5]
 *
 * 例 2:
 *
 * 入力: head = [], val = 1
 * 出力: []
 *
 * 例 3:
 *
 * 入力: head = [7,7,7,7], val = 7
 * 出力: []
 *
 *
 *
 * 制約:
 *
 * 	  - リスト内のノード数は `[0, 104]` の範囲。
 *
 * 	  - `1 <= Node.val <= 50`
 *
 * 	  - `0 <= val <= 50`
 */
package leetcode.p0203_remove_linked_list_elements;

import leetcode.common.ListNode;

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode removeElements(ListNode head, int val) {
        while (head != null && head.val == val) {
            head = head.next;
        }

        ListNode cur = head;
        
        while (cur != null && cur.next != null) {
            if (cur.next.val == val) {
                cur.next = cur.next.next;
            }else{
                cur = cur.next;
            }
            
        }
        return head;
    }
}
