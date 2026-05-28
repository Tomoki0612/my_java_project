package leetcode.p0232_implement_queue_using_stacks;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Implement Queue using Stacks [Easy]
class SolutionTest {

    @Test
    void example1() {
        MyQueue queue = new MyQueue();
        queue.push(1);
        queue.push(2);
        assertEquals(1, queue.peek());
        assertEquals(1, queue.pop());
        assertFalse(queue.empty());
    }
}
