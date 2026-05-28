/*
 * Palindrome Linked List
 * Difficulty: Easy
 * https://leetcode.com/problems/palindrome-linked-list/
 *
 * Given the `head` of a singly linked list, return `true` if it is a
 * palindrome or `false` otherwise.
 *
 *
 *
 * Example 1:
 *
 * Input: head = [1,2,2,1]
 * Output: true
 *
 * Example 2:
 *
 * Input: head = [1,2]
 * Output: false
 *
 *
 *
 * Constraints:
 *
 * 	  - The number of nodes in the list is in the range `[1, 105]`.
 *
 * 	  - `0 <= Node.val <= 9`
 *
 *
 *
 * Follow up: Could you do it in `O(n)` time and `O(1)` space?
 */
package leetcode.p0234_palindrome_linked_list;

import java.util.ArrayDeque;
import java.util.Deque;

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
    public boolean isPalindrome(ListNode head) {
        ListNode cur = head;
        Deque<Integer> stack = new ArrayDeque<>();
        while (cur != null) {
            stack.push(cur.val);
            cur = cur.next;
        }
        cur = head;
        while (!stack.isEmpty()) {
            if (cur.val != stack.pop()) {
                return false;
            }
            cur = cur.next;
        }
        return true;
    }
}
