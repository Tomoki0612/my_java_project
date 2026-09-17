/*
 * Binary Tree Paths
 * Difficulty: Easy
 * https://leetcode.com/problems/binary-tree-paths/
 *
 * You are given the `root` of a binary tree.
 *
 * Return all root-to-leaf paths in any order.
 *
 * A leaf is a node with no children.
 *
 *
 *
 * Example 1:
 *
 * Input: root = [1,2,3,null,5]
 * Output: ["1->2->5","1->3"]
 *
 * Example 2:
 *
 * Input: root = [1]
 * Output: ["1"]
 *
 *
 *
 * Constraints:
 *
 * 	  - The number of nodes in the tree is in the range `[1, 100]`.
 *
 * 	  - `-100 <= Node.val <= 100`
 */
package leetcode.p0257_binary_tree_paths;

import java.util.ArrayList;
import java.util.List;

import leetcode.common.TreeNode;

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> list = new ArrayList<>();
        String paths = "";
        dfs(root, list, paths);
        return list;
    }

    private void dfs(TreeNode node, List<String> list ,String paths){
        paths += node.val;
        if (node.left == null && node.right == null) {
            list.add(paths);
        }

        if (node.left != null) {
            dfs(node.left, list, paths + "->");
        }

        if (node.right != null) {
            dfs(node.right, list, paths + "->");
        }
    }
}
