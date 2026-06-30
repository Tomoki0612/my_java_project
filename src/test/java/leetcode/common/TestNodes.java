package leetcode.common;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;

public final class TestNodes {
    private TestNodes() {
    }

    public static ListNode list(int... values) {
        ListNode dummy = new ListNode();
        ListNode cur = dummy;
        for (int value : values) {
            cur.next = new ListNode(value);
            cur = cur.next;
        }
        return dummy.next;
    }

    public static int[] toArray(ListNode head) {
        List<Integer> values = new ArrayList<>();
        ListNode cur = head;
        while (cur != null) {
            values.add(cur.val);
            cur = cur.next;
        }
        return values.stream().mapToInt(Integer::intValue).toArray();
    }

    public static ListNode nodeAt(ListNode head, int index) {
        ListNode cur = head;
        for (int i = 0; i < index && cur != null; i++) {
            cur = cur.next;
        }
        return cur;
    }

    public static ListNode tail(ListNode head) {
        if (head == null) {
            return null;
        }
        ListNode cur = head;
        while (cur.next != null) {
            cur = cur.next;
        }
        return cur;
    }

    public static ListNode listWithCycle(int[] values, int pos) {
        ListNode head = list(values);
        if (pos >= 0) {
            tail(head).next = nodeAt(head, pos);
        }
        return head;
    }

    public static TreeNode tree(Integer... values) {
        if (values.length == 0 || values[0] == null) {
            return null;
        }

        TreeNode root = new TreeNode(values[0]);
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        int i = 1;
        while (!queue.isEmpty() && i < values.length) {
            TreeNode node = queue.remove();
            if (i < values.length && values[i] != null) {
                node.left = new TreeNode(values[i]);
                queue.add(node.left);
            }
            i++;
            if (i < values.length && values[i] != null) {
                node.right = new TreeNode(values[i]);
                queue.add(node.right);
            }
            i++;
        }
        return root;
    }

    public static List<Integer> toLevelOrder(TreeNode root) {
        List<Integer> values = new ArrayList<>();
        if (root == null) {
            return values;
        }

        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            TreeNode node = queue.remove();
            if (node == null) {
                values.add(null);
            } else {
                values.add(node.val);
                queue.add(node.left);
                queue.add(node.right);
            }
        }

        int last = values.size() - 1;
        while (last >= 0 && values.get(last) == null) {
            values.remove(last);
            last--;
        }
        return values;
    }
}
