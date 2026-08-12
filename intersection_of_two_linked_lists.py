class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode | None:
        p1, p2 = headA, headB
        while p1 is not p2:
            p1 = p1.next if p1 else headB
            p2 = p2.next if p2 else headA
        return p1


if __name__ == "__main__":
    # headA: 4 -> 1 -> 8 -> 4 -> 5
    # headB: 5 -> 6 -> 1 -> 8 -> 4 -> 5
    # 相交于值为 8 的节点

    common = ListNode(8)
    common.next = ListNode(4)
    common.next.next = ListNode(5)

    headA = ListNode(4)
    headA.next = ListNode(1)
    headA.next.next = common

    headB = ListNode(5)
    headB.next = ListNode(6)
    headB.next.next = ListNode(1)
    headB.next.next.next = common

    sol = Solution()
    result = sol.getIntersectionNode(headA, headB)
    print(f"相交节点值: {result.val if result else 'None'}")  # 期望: 8

    # 测试不相交的情况
    headC = ListNode(1)
    headC.next = ListNode(2)

    headD = ListNode(3)
    headD.next = ListNode(4)

    result2 = sol.getIntersectionNode(headC, headD)
    print(f"不相交情况: {result2.val if result2 else 'None'}")  # 期望: None

    """
    今天继续研究算法，是一个链表的题目，我对链表还不是很熟悉：相交链表 https://leetcode.cn/problems/intersection-of-two-linked-lists/description/

    题目：给你两个单链表的头节点 headA 和 headB ，请你找出并返回两个单链表相交的起始节点。如果两个链表不存在相交节点，返回 null 。你能否设计一个时间复杂度 O(m + n) 、仅用 O(1) 内存的解决方案？

    开始我想的思路是，既然要相交节点的值，那么从尾巴往前遍历不就很方便了。但是忽略了这不是数组，单链表没有 prev 指针，走不回头。不过可以将两个链表放入两个栈中同时弹出，只是空间多占了 O(n + m)，不符合题目要求。

    只能从头遍历的话那么我又想到了双层遍历，对比链表A和B中的每一个节点，引用相同则就是交点。这样时间复杂度是O(nm)不满足题目要求。
    ```python
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode | None:
        currentA = headA
        while currentA:
            currentB = headB
            while currentB:
                if currentA is currentB:
                    return currentA
                currentB = currentB.next
            currentA = currentA.next
        return None

    ```
    从前面做题的经验来说，一般遇到双层遍历要思考一下能不能用哈希表。在这个题中可以用但是不太适用，先将A中节点全部存进set，然后遍历B。这样第一个再set中出现的节点就是交点。这样的话时间复杂度减少到了O(n + m)，但是空间变成了 O(n)，也不符合题目要求。    

    ```python
        def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode | None:
        seen = set()
        currentA = headA
        while currentA:
            seen.add(currentA)
            currentA = currentA.next

        currentB = headB
        while currentB:
            if currentB in seen:
                return currentB
            currentB = currentB.next
        return None

    ```

    我想过使用双指针，但是不知道如何下手，链表的长度根本不一样。最后在AI的提示下得到了一个巧妙的方法：a和b长度不一样但是a + b 和b + a 的长度是相同的。
    一个指针从a出发，遍历完a再从b开始遍历，另一个指针遍历完b再从a开始遍历。如果两链表有交点，则会在交点相遇，如果没有则会同时走到None。

    关于为什么两指针会在交点相遇，我也是思考了有一会。结果发现，如果有交点，说明a和b的后半段是相同的，a和b拼接成等长的链表后，它们的后半段一定是对齐了，所以遍历到第一个相同的节点时，这个点就是交点。
    妙，太妙了。
    开始实操：
```python
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode | None:
        p1, p2 = headA, headB
        while p1 is not p2:
            p1 = p1.next if p1 else headB
            p2 = p2.next if p2 else headA
        return p1
```
    不仅代码简洁，复杂度也来到了O(n + m)和O(1)。很优雅，一个好的设计真的是妙不可言！
    """
