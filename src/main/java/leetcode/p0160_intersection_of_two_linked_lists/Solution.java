/*
 * Intersection of Two Linked Lists
 * Difficulty: Easy
 * https://leetcode.com/problems/intersection-of-two-linked-lists/
 *
 * 2つの単方向連結リストの先頭 `headA` と `headB` が与えられます。
 * 2つのリストが交差するノードを返してください。
 * 交差がない場合は `null` を返してください。
 *
 * たとえば、以下の2つの連結リストはノード `c1` で交差し始めます。
 *
 * テストケースは、リスト構造全体にサイクルが存在しないように生成されます。
 *
 * 関数が返った後も、連結リストは元の構造を保持していなければなりません。
 *
 * カスタムジャッジ:
 *
 * ジャッジへの入力は以下のように与えられます（あなたのプログラムにはこれらの入力は渡されません）:
 *
 * - `intersectVal` - 交差が発生するノードの値。交差するノードがない場合は `0`。
 * - `listA` - 1つ目の連結リスト。
 * - `listB` - 2つ目の連結リスト。
 * - `skipA` - 交差ノードに到達するために `listA` の先頭からスキップするノード数。
 * - `skipB` - 交差ノードに到達するために `listB` の先頭からスキップするノード数。
 *
 * ジャッジはこれらの入力をもとに連結構造を作成し、
 * 2つの先頭 `headA` と `headB` をあなたのプログラムに渡します。
 * 交差ノードを正しく返せば、解答は受理されます。
 *
 * ---
 *
 * 例 1:
 *
 * ```
 * Input: intersectVal = 8, listA = [4,1,8,4,5], listB = [5,6,1,8,4,5], skipA
 * = 2, skipB = 3
 * Output: Intersected at '8'
 * ```
 * 説明: 交差ノードの値は 8 です（2つのリストが交差する場合、この値は 0 であってはなりません）。
 * A の先頭からは [4,1,8,4,5]、B の先頭からは [5,6,1,8,4,5] と読めます。
 * A では交差ノードの前に 2 ノード、B では 3 ノードがあります。
 * - 交差ノードの値が 1 でない点に注意してください。
 *   A の 2 番目のノードと B の 3 番目のノードはどちらも値が 1 ですが、
 *   異なるノード参照（異なるメモリ上の場所）を指しています。
 *   一方、A の 3 番目と B の 4 番目のノード（値 8）は同じメモリ上の場所を指しています。
 *
 * 例 2:
 *
 * ```
 * Input: intersectVal = 2, listA = [1,9,1,2,4], listB = [3,2,4], skipA = 3,
 * skipB = 1
 * Output: Intersected at '2'
 * ```
 * 説明: 交差ノードの値は 2 です。
 * A の先頭からは [1,9,1,2,4]、B の先頭からは [3,2,4] と読めます。
 * A では交差ノードの前に 3 ノード、B では 1 ノードがあります。
 *
 * 例 3:
 *
 * ```
 * Input: intersectVal = 0, listA = [2,6,4], listB = [1,5], skipA = 3, skipB =
 * 2
 * Output: No intersection
 * ```
 * 説明: A の先頭からは [2,6,4]、B の先頭からは [1,5] と読めます。
 * 2つのリストは交差しないため、`intersectVal` は 0 でなければなりません。
 * `skipA` と `skipB` は任意の値をとれます。
 * 2つのリストは交差しないので、`null` を返してください。
 *
 * ---
 *
 * 制約:
 *
 * - `listA` のノード数は `m`。
 * - `listB` のノード数は `n`。
 * - `1 <= m, n <= 3 * 10^4`
 * - `1 <= Node.val <= 10^5`
 * - `0 <= skipA <= m`
 * - `0 <= skipB <= n`
 * - `listA` と `listB` が交差しない場合、`intersectVal` は `0`。
 * - `listA` と `listB` が交差する場合、`intersectVal == listA[skipA] == listB[skipB]`。
 *
 * ---
 *
 * フォローアップ: `O(m + n)` の時間計算量かつ `O(1)` のメモリ使用量で解けますか？
 */
package leetcode.p0160_intersection_of_two_linked_lists;
import leetcode.common.*;

/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode(int x) {
 *         val = x;
 *         next = null;
 *     }
 * }
 */
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode cur_A = headA;
        ListNode cur_B = headB; 
        while (cur_A != null) {
            while (cur_B != null) {
                if (cur_A == cur_B) {
                    return cur_A;
                }
                cur_B = cur_B.next;
            }
            cur_B = headB;
            cur_A = cur_A.next;
        }
        return null;
    }
}
