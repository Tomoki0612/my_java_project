package leetcode.p0225_implement_stack_using_queues;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

// Implement Stack using Queues [Easy]
class SolutionTest {

    @Test
    void example1() {
        MyStack stack = new MyStack();
        stack.push(1);
        stack.push(2);
        assertEquals(2, stack.top());
        assertEquals(2, stack.pop());
        assertFalse(stack.empty());
    }
}
