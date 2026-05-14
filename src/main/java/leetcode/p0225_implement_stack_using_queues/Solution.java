/*
 * Implement Stack using Queues
 * Difficulty: Easy
 * https://leetcode.com/problems/implement-stack-using-queues/
 *
 * 2つのキューだけを使って、後入れ先出し（LIFO）スタックを実装してください。
 * 実装するスタックは通常のスタックのすべての機能
 * （`push`、`top`、`pop`、`empty`）をサポートする必要があります。
 *
 * `MyStack` クラスを実装してください：
 *
 * 	  - `void push(int x)` 要素 x をスタックの先頭にプッシュします。
 *
 * 	  - `int pop()` スタックの先頭の要素を取り除き、それを返します。
 *
 * 	  - `int top()` スタックの先頭の要素を返します。
 *
 * 	  - `boolean empty()` スタックが空なら `true`、
 * 	    そうでなければ `false` を返します。
 *
 * 注意事項：
 *
 * 	  - キューの標準的な操作のみを使用しなければなりません。
 * 	    つまり、`push to back`、`peek/pop from front`、`size`、`is empty` の
 * 	    操作のみが有効です。
 *
 * 	  - 言語によっては、キューがネイティブにサポートされていない場合があります。
 * 	    キューの標準操作のみを使用する限り、
 * 	    リストや deque（両端キュー）を使ってキューをシミュレートしても構いません。
 *
 *
 *
 * Example 1:
 *
 * Input
 * ["MyStack", "push", "push", "top", "pop", "empty"]
 * [[], [1], [2], [], [], []]
 * Output
 * [null, null, null, 2, 2, false]
 *
 * Explanation
 * MyStack myStack = new MyStack();
 * myStack.push(1);
 * myStack.push(2);
 * myStack.top(); // return 2
 * myStack.pop(); // return 2
 * myStack.empty(); // return False
 *
 *
 *
 * Constraints:
 *
 * 	  - `1 <= x <= 9`
 *
 * 	  - `push`、`pop`、`top`、`empty` への呼び出しは最大で `100` 回です。
 *
 * 	  - `pop` と `top` への呼び出しはすべて有効です。
 *
 *
 *
 * Follow-up: 1つのキューだけを使ってスタックを実装できますか？
 */
package leetcode.p0225_implement_stack_using_queues;

class MyStack {

    public MyStack() {
        return false;
    }
    
    public void push(int x) {
        return false;
    }
    
    public int pop() {
        return false;
    }
    
    public int top() {
        return false;
    }
    
    public boolean empty() {
        return false;
    }
}

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack obj = new MyStack();
 * obj.push(x);
 * int param_2 = obj.pop();
 * int param_3 = obj.top();
 * boolean param_4 = obj.empty();
 */
