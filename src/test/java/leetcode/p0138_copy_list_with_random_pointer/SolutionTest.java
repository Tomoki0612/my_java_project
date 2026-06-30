package leetcode.p0138_copy_list_with_random_pointer;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;

// Copy List with Random Pointer [Medium]
class SolutionTest {
    private final Solution solution = new Solution();

    @Test
    void example1() {
        assertDeepCopy(
            build(new int[][]{{7, -1}, {13, 0}, {11, 4}, {10, 2}, {1, 0}}),
            new int[][]{{7, -1}, {13, 0}, {11, 4}, {10, 2}, {1, 0}}
        );
    }

    @Test
    void example2() {
        assertDeepCopy(
            build(new int[][]{{1, 1}, {2, 1}}),
            new int[][]{{1, 1}, {2, 1}}
        );
    }

    @Test
    void example3() {
        assertDeepCopy(
            build(new int[][]{{3, -1}, {3, 0}, {3, -1}}),
            new int[][]{{3, -1}, {3, 0}, {3, -1}}
        );
    }

    @Test
    void emptyList() {
        assertNull(solution.copyRandomList(null));
    }

    private void assertDeepCopy(Node original, int[][] expectedPairs) {
        Node copy = solution.copyRandomList(original);
        assertArrayEquals(expectedPairs, toPairs(copy));

        Node curOriginal = original;
        Node curCopy = copy;
        while (curOriginal != null) {
            assertNotSame(curOriginal, curCopy);
            if (curOriginal.random != null) {
                assertNotSame(curOriginal.random, curCopy.random);
                assertEquals(curOriginal.random.val, curCopy.random.val);
            } else {
                assertNull(curCopy.random);
            }
            curOriginal = curOriginal.next;
            curCopy = curCopy.next;
        }
    }

    private Node build(int[][] pairs) {
        if (pairs.length == 0) {
            return null;
        }

        Node[] nodes = new Node[pairs.length];
        for (int i = 0; i < pairs.length; i++) {
            nodes[i] = new Node(pairs[i][0]);
        }
        for (int i = 0; i < pairs.length - 1; i++) {
            nodes[i].next = nodes[i + 1];
        }
        for (int i = 0; i < pairs.length; i++) {
            int randomIndex = pairs[i][1];
            if (randomIndex >= 0) {
                nodes[i].random = nodes[randomIndex];
            }
        }
        return nodes[0];
    }

    private int[][] toPairs(Node head) {
        List<Node> nodes = new ArrayList<>();
        for (Node cur = head; cur != null; cur = cur.next) {
            nodes.add(cur);
        }

        Map<Node, Integer> indexes = new IdentityHashMap<>();
        for (int i = 0; i < nodes.size(); i++) {
            indexes.put(nodes.get(i), i);
        }

        int[][] pairs = new int[nodes.size()][2];
        for (int i = 0; i < nodes.size(); i++) {
            Node node = nodes.get(i);
            pairs[i][0] = node.val;
            pairs[i][1] = node.random == null ? -1 : indexes.get(node.random);
        }
        return pairs;
    }
}
