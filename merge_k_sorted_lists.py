import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        heap = []

        for head in lists:
            if head:
                heapq.heappush(heap, (head.val, id(head), head))

        result = ListNode()
        p = result

        while heap:
            val, nodeId, node = heapq.heappop(heap)
            p.next = node
            p = p.next
            if node.next:
                heapq.heappush(heap, (node.next.val, id(node.next), node.next))

        return result.next


if __name__ == "__main__":
    # 测试 1: [[1,4,5],[1,3,4],[2,6]]
    # 期望: [1,1,2,3,4,4,5,6]
    l1 = ListNode(1, ListNode(4, ListNode(5)))
    l2 = ListNode(1, ListNode(3, ListNode(4)))
    l3 = ListNode(2, ListNode(6))
    sol = Solution()
    result = sol.mergeKLists([l1, l2, l3])
    print("测试 1:")
    nodes = []
    while result:
        nodes.append(str(result.val))
        result = result.next
    print(" -> ".join(nodes))  # 期望: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6

    # 测试 2: 空列表
    result2 = sol.mergeKLists([])
    print(f"\n测试 2 (空列表): {result2}")  # 期望: None

    # 测试 3: 只含一个空链表
    result3 = sol.mergeKLists([None])
    print(f"测试 3 (空链表): {result3}")  # 期望: None

    """
    今天尝试：[合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/description/)

    给你一个链表数组，每个链表都已经按升序排列。
    请你将所有链表合并到一个升序链表中，返回合并后的链表。

    ## 数组排序

    思考半天没有头绪，试试暴力解法：遍历链表将所有节点放入一个数组，排序后转成新的链表返回。

    ```python
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        dummy = ListNode()
        tail = dummy

        nums = []

        for item in lists:  # 遍历加入数组
            head = item
            while head:
                nums.append(head.val)
                head = head.next

        nums.sort()  # 排序

        for i in nums:  # 创建新链表
            tail.next = ListNode(i)
            tail = tail.next

        return dummy.next
    ```
    比较取巧，利用了 Python 本身的排序。
    时间复杂度：$O(N \log N)$，`N` 是所有节点总数。空间：$O(N)$（`nums` 数组）。

    这里并没用到"每条链表本身已经有序"这个条件。因为链表有序，就可以从链表头开始，将两个链表中较小的元素放到新的链表中，这样两条链表可以合成一个新的有序链表。

    ## 两两合并与分治法

    试试两两合并的方法，先取两条链表，合成一条新链表，再去合并下一条。
    先写一个通用的将两条有序链表合并成一条的方法 `mergeTwo`，再遍历链表数组，将每一条与之前合并过的链表进行合并。

    ```python
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        result = None
        for head in lists:
            result = self.mergeTwo(result, head)
        return result

    def mergeTwo(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 or l2  # 其中一条遍历完后将另一条接到 dummy 上
        return dummy.next
    ```
    时间复杂度为 $O(NK)$，`N` 为节点总数，`K` 为链表条数。因为每条链表合并时，`result` 越来越长，每条后面的链表都要和前面所有节点比较。如果 `K` 条链表长度接近，总比较次数约等于 $N \times K$。空间为 $O(1)$——只用了 `mergeTwo` 中的哨兵节点，不随数据规模增长。

    既然是两两合并，那么每次取一条来合并不如像淘汰赛一样，先两两合并，之后将它们的结果再进行合并。这就是分治法。

    ```python
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        if not lists:
            return None

        while len(lists) > 1:
            merged = []
            for i in range(0, len(lists), 2):  # 步长为 2
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged.append(self.mergeTwo(l1, l2))
            lists = merged

        return lists[0]

    def mergeTwo(self, l1, l2):
        dummy = ListNode()
        tail = dummy
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 or l2  # 其中一条遍历完后将另一条接到 dummy 上
        return dummy.next
    ```
    时间复杂度为 $O(N \log K)$。每轮合并的节点总数固定为 `N`，共 $\log K$ 轮，所以总操作次数为 $N \log K$。空间为 $O(1)$（非递归写法，不计结果链表）。

    ## 堆

    正统思路其实是用小顶堆，每次只比较 `K` 个链表头节点，挑最小的插入。

    创建一个大小为 `K` 的堆，`K` 为链表的条数。因为链表已经有序，每次都能将当前最小的推进堆中。堆弹出最小的一个放到新链表，再从对应链表中推入下一个节点继续比较。

    只将节点放入堆中是不行的，因为我们的节点没有实现比较方法。所以需要放进堆中的是节点值和节点组成的一个元组——节点值用于比较大小，节点用于在弹出后将其 `next` 推入堆中。
    但是还有一个问题：如果堆中的两个元组的节点值相等，那么堆又会继续比较元组的第二项（也就是我们的节点），这是不行的。所以元组还需要在节点值后面再加上一项来避免堆比较我们的节点。我们可以用链表在 `lists` 中的下标来区分，或者更省事直接使用 `id(node)`——它返回对象在内存中的唯一地址（整数）。

    思路是这样，但是一下手就卡住了：如何将 `K` 条链表塞进堆中呢？
    一条链表塞完再塞另一条链表是不行的，必须每条链表各塞一个最小的，才能达到全局排序的效果。
    我最开始使用的是遍历数组的思维，发现怎么都不好遍历。后面发现只需要在堆弹出某个节点时，将这个节点的 `next` 推入堆中就行了。

    先将每个链表的头节点放进堆中，每次遍历先从堆中弹出堆顶放进新链表，然后将它的 `next` 节点放进堆中，一直循环到没有新的节点进入堆、堆中的元素全部弹空为止。最后得到的新链表就是我们要的升序链表。

    代码实现：
    ```python
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        heap = []

        # 初始化堆，将每个链表的头节点放进堆中
        for head in lists:
            if head:
                heapq.heappush(heap, (head.val, id(head), head))

        result = ListNode()
        p = result

        while heap:
            val, nodeId, node = heapq.heappop(heap)
            p.next = node
            p = p.next
            if node.next:
                heapq.heappush(heap, (node.next.val, id(node.next), node.next))

        return result.next
    ```
    时间复杂度是 $O(N \log K)$。每个节点最多进堆一次、出堆一次，每次堆操作（`heappush` / `heappop`）的复杂度为 $O(\log K)$，`N` 个节点总共 $O(N \log K)$。空间为 $O(K)$——堆最多同时存储 `K` 个元素。

    堆和分治都是 $O(N \log K)$，区别在常数和空间：
    - 堆：空间 $O(K)$
    - 分治：空间 $O(1)$（递归算栈的话 $O(\log K)$）

    """
