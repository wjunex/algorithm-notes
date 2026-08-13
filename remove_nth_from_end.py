from collections import deque


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
        dummy = ListNode(0, head)
        cur = dummy
        window = deque()
        while cur:
            window.append(cur)
            if len(window) > n + 1:
                window.popleft()
            cur = cur.next
        window[0].next = window[0].next.next
        return dummy.next


if __name__ == "__main__":
    # 辅助函数：链表转列表
    def to_list(head):
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result

    # 辅助函数：列表转链表
    def to_linked_list(lst):
        dummy = ListNode()
        tail = dummy
        for v in lst:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next

    test_cases = [
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5], "删除倒数第2个"),
        ([1], 1, [], "只有一个节点"),
        ([1, 2], 1, [1], "两个节点，删最后一个"),
        ([1, 2], 2, [2], "两个节点，删第一个（即倒数第2）"),
    ]

    sol = Solution()
    for nums, n, expected, desc in test_cases:
        head = to_linked_list(nums)
        result = sol.removeNthFromEnd(head, n)
        output = to_list(result)
        print(f"输入: {nums}, n={n}")
        print(f"期望: {expected}, 实际: {output}")
        print(f"描述: {desc}")
        print("-" * 40)

"""
今天继续尝试：[删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/description/)

给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。

我的想法是：使用两个指针，让它们相隔 `n` 个节点，然后同时向后移动。当后面的快指针到达链表末尾时，慢指针的位置就是待删节点的前驱。

```python
def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next

    while fast.next:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next

    return dummy.next
```

这里使用哨兵节点的原因是为了方便删除节点，比如 `n` 等于链表长度时需要删除头节点，不使用哨兵节点的话无法操作。

使用双指针，一趟扫描完，$O(n)$ 时间 $O(1)$ 空间。

既然双指针类似一个固定大小的窗口，那么我想到了可以使用一个固定大小的队列来尝试解决。

同理，也需要用到哨兵节点，所以队列的长度应该是 `n + 1`。

```python
def removeNthFromEnd(self, head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(0, head)
    cur = dummy
    window = deque()
    while cur:
        window.append(cur)
        if len(window) > n + 1:
            window.popleft()
        cur = cur.next
    window[0].next = window[0].next.next
    return dummy.next
```

时间 $O(n)$：每个节点进队一次、出队一次，都是 $O(1)$，一趟遍历。
空间 $O(n)$：`window` 最多存 `n + 1` 个节点。

除此之外还有两个解法：
- 一种是先遍历得到链表长度，第二次遍历再删除目标节点。时间 $O(n)$，空间 $O(1)$，但要走两遍。
- 一种是将链表依次压入栈中，再弹出 `n` 个节点。时间 $O(n)$，空间 $O(n)$。

所以，我一开始想到的使用双指针的方法就已经是这个题的最优解了。
"""
