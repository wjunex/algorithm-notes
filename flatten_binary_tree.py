from typing import Optional
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        node = root
        while node:
            if node.left:
                # 1. 找左子树最右下节点，就是展开成链后的尾巴
                tail = node.left
                while tail.right:
                    tail = tail.right
                # 2. 尾巴接上右子树
                tail.right = node.right
                # 3. 左子树整体搬到右边，左指针清空
                node.right = node.left
                node.left = None
            # 前进到下一个节点
            node = node.right


def build_tree(values):
    """按层序遍历的列表构造二叉树，None 表示空节点"""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while i < len(values):
        node = q.popleft()
        if values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


def to_list(root):
    """展开后一路向右收集 val，若左指针未清空则返回 None 表示出错"""
    result = []
    node = root
    while node:
        if node.left is not None:
            return None
        result.append(node.val)
        node = node.right
    return result


if __name__ == "__main__":
    test_cases = [
        ([1, 2, 5, 3, 4, None, 6], [1, 2, 3, 4, 5, 6], "标准例子"),
        ([1], [1], "单节点"),
        ([], [], "空树"),
        ([1, 2, None, 3], [1, 2, 3], "只有左子树"),
        ([1, None, 2, None, 3], [1, 2, 3], "只有右子树"),
    ]

    sol = Solution()
    for values, expected, desc in test_cases:
        root = build_tree(values)
        sol.flatten(root)
        output = to_list(root)
        print(f"输入: {values}")
        print(f"期望: {expected}, 实际: {output}")
        print(f"描述: {desc}")
        print("-" * 40)

"""
今天继续研究算法：[二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/description/)

给你二叉树的根结点 `root`，请你将它展开为一个单链表：展开后的单链表应该同样使用 `TreeNode`，其中 `right` 子指针指向链表中下一个结点，而左子指针始终为 `null`。展开后的单链表应该与二叉树 `先序遍历` 顺序相同。
进阶：你可以使用原地算法（O(1) 额外空间）展开这棵树吗？

看到这个题我的头就开始痛了，因为好久没接触树了，连遍历方法都忘得一干二净了，不过既然遇到了那就把它解决掉，长痛不如短痛。

## 遍历树

先捡一下遍历方法：
```python
def preorder(root):
    if not root:          # 基线条件：走到空节点就回头
        return
    print(root.val)       # 1. 先处理根
    preorder(root.left)   # 2. 再处理左子树
    preorder(root.right)  # 3. 再处理右子树
```
树的遍历代码，本质就一个套路：每个节点都做三件事——处理「自己」（根）、处理「左子树」、处理「右子树」。所谓先序、中序、后序，区别只是这三件事谁先谁后：先序（根左右）、中序（左根右）、后序（左右根）。

## 暴力破解
既然题目要求的是先序，那么我们直接将树按照先序遍历，将节点放进一个数组中。然后遍历这个数组，将每个节点的右节点改成数组下一项，左节点置为 `None`。
```python
def flatten(self, root: Optional[TreeNode]) -> None:
    nodes = []
    self._preorder(root, nodes)
    for i, item in enumerate(nodes):
        item.right = nodes[i + 1] if i < len(nodes) - 1 else None
        item.left = None

def _preorder(self, root, nodes):
    if not root:
        return
    nodes.append(root)
    self._preorder(root.left, nodes)
    self._preorder(root.right, nodes)
```
复杂度是时间 $O(n)$、空间 $O(n)$（`nodes` 列表占了 $n$ 个节点）。

题目的进阶要求是 $O(1)$ 的额外空间，那就得换个思路。

## 原地展开

实在没有头绪，直接看了题解，原理其实很简单：从根节点开始一路向右扫，每遇到一个有左子树的节点，就把它「拉直」：
1. 找到它左子树里一路向右走到底的节点，也就是左子树展开成链后的尾巴。
2. 把当前节点的右子树整段接到尾巴的 `right` 上。
3. 把左子树整体搬到右边，即 `node.right = node.left`。
4. 清空左指针，即 `node.left = None`。

然后前进到下一个节点（`node = node.right`），重复上面的动作。左子树的链尾始终接着右子树，一路拉直，整棵树就成了一条链。

```python
def flatten(self, root: Optional[TreeNode]) -> None:
    node = root
    while node:
        if node.left:
            # 1. 找左子树最右下节点，就是展开成链后的尾巴
            tail = node.left
            while tail.right:
                tail = tail.right
            # 2. 尾巴接上右子树
            tail.right = node.right
            # 3. 左子树整体搬到右边，左指针清空
            node.right = node.left
            node.left = None
        # 前进到下一个节点
        node = node.right
```

时间 $O(n)$：外层 `while` 每个节点走一次，内层「找尾巴」的 `while` 看似嵌套，但整条右链每个节点总共只被扫常数次，摊下来仍是线性。

空间 $O(1)$：只用了 `node`、`tail` 两个指针，原地改树。
"""
