package leetcode.p0160_intersection_of_two_linked_lists;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import leetcode.common.ListNode;
import static leetcode.common.TestNodes.list;
import static leetcode.common.TestNodes.nodeAt;
import static leetcode.common.TestNodes.tail;

// Intersection of Two Linked Lists [Easy]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        ListNode shared = list(8, 4, 5);
        ListNode headA = list(4, 1);
        ListNode headB = list(5, 6, 1);
        tail(headA).next = shared;
        tail(headB).next = shared;

        assertSame(shared, solution.getIntersectionNode(headA, headB));
    }

    @Test
    void example2() {
        ListNode shared = list(2, 4);
        ListNode headA = list(1, 9, 1);
        ListNode headB = list(3);
        tail(headA).next = shared;
        tail(headB).next = shared;

        assertSame(shared, solution.getIntersectionNode(headA, headB));
    }

    @Test
    void example3() {
        assertNull(solution.getIntersectionNode(list(2, 6, 4), list(1, 5)));
    }

    @Test
    void intersectsAfterFirstNode() {
        ListNode headA = list(1, 2, 3);
        ListNode headB = list(9);
        ListNode shared = nodeAt(headA, 1);
        tail(headB).next = shared;

        assertSame(shared, solution.getIntersectionNode(headA, headB));
    }
}
