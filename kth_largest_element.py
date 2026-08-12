import heapq, random


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        # 使用一个新的方法，支持传入下标方便我们操作数组
        return self._quick_select(nums, 0, len(nums) - 1, k)

    def _quick_select(self, nums, left, right, k):
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]  # 随机换到最后
        pivot = nums[right]

        lt = left
        eq = left
        for j in range(left, right):
            if nums[j] > pivot:
                nums[j], nums[eq] = nums[eq], nums[j]
                # 遇到大的先放到相等区的最右边eq处
                nums[eq], nums[lt] = nums[lt], nums[eq]
                # 与大数区最右边的处的lt交换
                # 这样lt的左边全是大数，eq的左边全是等于pivot的，剩下的就是小于pivot的
                lt += 1
                eq += 1
            elif nums[j] == pivot:
                nums[j], nums[eq] = nums[eq], nums[j]
                eq += 1
        nums[eq], nums[right] = nums[right], nums[eq]
        # 遍历完后pivot放到相等分区处，
        eq += 1  # eq指向小区开头

        if k <= lt - left:  # 落在大区
            return self._quick_select(nums, left, lt - 1, k)
        elif k <= eq - left:
            # 不管落在相等区的那个位置，直接返回pivot
            return pivot
        else:  # 落在小区
            return self._quick_select(nums, eq, right, k - (eq - left))
            # 下次找的k为这次的k减去eq之前的长度，这个长度就是eq所在的位置减去left


if __name__ == "__main__":
    test_cases = [
        ([3, 2, 1, 5, 6, 4], 2, 5, "标准例子"),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4, "含重复元素"),
        ([1], 1, 1, "单元素"),
        ([7, 6, 5, 4, 3, 2, 1], 5, 3, "降序"),
    ]

    sol = Solution()
    for nums, k, expected, desc in test_cases:
        output = sol.findKthLargest(nums, k)
        print(f"数组: {nums}, k: {k}")
        print(f"期望: {expected}, 实际: {output}")
        print(f"描述: {desc}")
        print("-" * 40)


"""
今天尝试：数组中的第 K 个最大元素：https://leetcode.cn/problems/kth-largest-element-in-an-array/description/

给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。

## 普通排序

第一眼没认真读题——返回数组第 k 大的，那不就是排序后直接返回 nums[k-1] 不就行了。

```python
def findKthLargest(self, nums: list[int], k: int) -> int:
    nums.sort(reverse=True)
    return nums[k - 1]
```
提交通过，正好奇这个题为什么这么简单，仔细看题发现要求时间复杂度为 O(n)，而我们使用的 sort 排序的复杂度是 O(n log n)。

## 堆

遇到知识盲区了，AI 给出了两种方案，先看一下第一种：使用堆。
堆是一棵完全二叉树，满足"父节点比所有子节点小（或大）"。小顶堆的根（堆顶）永远是全局最小值，大顶堆的根是最大值。Python 的 heapq 默认是小顶堆。
插入和弹出后，堆会自动调整（上浮/下沉，O(log n)），始终保证堆顶是极值。每次弹出只需直接拿堆顶即可，不需要遍历整个堆。
通俗地说，元素放入堆中后会自动排序（堆不是"全排序"，而是"部分有序"——只保证堆顶是最小值，堆内部不是从大到小排列的）。我们只需要遍历数组，将元素放进一个大小为 k 的堆中，超出 k 后，将里面最小的元素弹出。遍历完数组后，最终堆中就剩下了最大的 k 个数，这时候堆顶的数最小，就是我们需要找的第 k 个最大的数。

```python
import heapq

def findKthLargest(self, nums: list[int], k: int) -> int:
    heap = []
    for item in nums:
        if len(heap) >= k:
            heapq.heappushpop(heap, item) # 将 item 加入堆后弹出堆顶
        else:
            heapq.heappush(heap, item) # 将 item 加入堆
    return heapq.heappop(heap) # 弹出堆顶
```
堆内部排序的复杂度是 O(log k)，所以我们的时间复杂度是 O(n log k)。堆要存 k 个元素，所以空间复杂度是 O(k)。

是一个很巧妙的方法，但是时间复杂度还是没有达到 O(n)，接下来尝试一下快速选择的方法。

## 快速选择

思路就是：随便选一个元素来快速排序，将数组中比它大的放它左边，比它小的放它右边。最后根据它的下标看它是第几大，如果正好是第 k 大，那么直接返回即可。
如果它的位置比 k 小，那么就要在它后面的数组中继续寻找第 (k - 它的位置) 大的数。如果它的位置比 k 大，那么就在它前面的数组中继续寻找第 k 大的数。

```python
def findKthLargest(self, nums: list[int], k: int) -> int:
    pivot = nums[-1]  # 找准一个基点，用于快速排序，这里使用数组最后一项
    i = 0
    for j in range(len(nums) - 1):  # 遍历不包含基点的数组
        if nums[j] >= pivot:
            nums[i], nums[j] = nums[j], nums[i]  # 将比基点大的数放到数组前面
            i += 1
    nums[i], nums[-1] = (
        nums[-1],
        nums[i],
    )  # 遍历完后将基点换到 i 处，这时候前面的数都比基点大，后面的数都比基点小

    if i == k - 1:
        # 这时候基点所在的位置 i，就是第 i+1 大，如果等于 k，那么基点就是第 k 大的数，直接 return 这个数即可
        return nums[i]
    elif i < k - 1:
        # 如果基点在 k 前面，说明需要在 i 后面的数组中继续寻找第 k 大的，递归 i 后方数组，k 在 i 后面，所以要递归的 k 是 k - (i + 1)，在子数组中寻找第 k - i - 1 大的数
        return self.findKthLargest(nums[i + 1 :], k - i - 1)
    elif i > k - 1:
        # 如果基点在 k 后面，说明需要在 i 前面的数组中继续寻找第 k 大的，递归 i 前方数组，k 在 i 前面所以不变
        return self.findKthLargest(nums[:i], k)
```
平均情况下，每轮递归的数组长度会比上一轮少一半，时间复杂度约为 O(2n) = O(n)。
最坏情况下，每次都选择到极大值或极小值，每次下次迭代的数组都只能排除掉一个元素，时间复杂度为 O(n²)。
随机选 pivot 可以把最坏概率压到极低。

## 算法优化

由于递归时使用的是切片，所以最坏情况下的空间复杂度是 O(n²)。
在提交时遇到了一个很刁钻的测试用例，果然超出了内存限制：nums=[1,2,3,4,5,超级多个1,-5,-4,-3,-2,-1]，k=50000。

继续优化——不使用切片。每轮的遍历在上一轮递归给出的区间上遍历，这样就不用使用额外的空间。
```python
def findKthLargest(self, nums: list[int], k: int) -> int:
    # 使用一个新的方法，支持传入下标方便我们操作数组
    return self._quick_select(nums, 0, len(nums) - 1, k)

def _quick_select(self, nums, left, right, k):
    i, pivot = left, nums[right]  # 仍然从最右边取 pivot
    for j in range(left, right):
        if nums[j] >= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[right] = nums[right], nums[i]

    if i == left + k - 1:
        # 原先在子数组中，i 始终从 0 开始，而现在的 i 是 nums 数组的一个下标，是从 left 开始的。
        # 所以现在第 i+1 大的数实际上是子数组中的 k + left 大的数，即 i = left + k - 1（由第几大转成下标）
        return nums[i]
    elif i < left + k - 1:
        return self._quick_select(nums, i + 1, right, k - (i - left + 1))
        # 要找的数在右边的子数组中，下轮要找的 k 是当前轮的 k - 本轮 for 循环中 i 增长的数 (i-left) 再加上 1（由下标转成第几大）
    else:
        return self._quick_select(nums, left, i - 1, k)
        # 原来的 [:i] 不含 i，而现在下标是包含的，所以需要 i - 1
```

不使用切片之后，空间复杂度来到了 O(log n)，在最坏情况下为 O(n)，节省下了不少的空间。

但是呢，就刚才那个刁钻的测试用例上又卡住了，超出了时间限制——因为每次获取的 pivot 都是从数组的最右边获取，遇到了最坏的情况，时间复杂度来到了 O(n²)。

试试随机 pivot：在给 pivot 赋值之前，随机从数组中抽一个数放到最后，那么就得到了随机的 pivot。
```python
    pivot_idx = random.randint(left, right)
    nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]  # 随机换到最后

    i, pivot = left, nums[right]  # 仍然从最右边取 pivot
```

节省了一点时间，但还是超时。发现 `if nums[j] >= pivot:` 这个判断条件会将所有相同的元素都扔到左边，就会有大量交换，而这个测试用例中就有大量相同的元素。
去掉等号，但还是超时。
原因是当数组有几千个 1，pivot 随机到 1 的概率极高。用 `>` 时，所有 1 原地不动，只排除了 pivot 自己，递归层数 = 重复元素的个数，依然是 O(n²)。

## 三路分区

现在只进行了两个分区——大的在左边，小的在右边——没有处理相同的元素，所以在这个刁钻的用例上被硬控了。现在改成三个分区：大的放左边，小的放右边，相等的放中间。

```python
def findKthLargest(self, nums: list[int], k: int) -> int:
    # 使用一个新的方法，支持传入下标方便我们操作数组
    return self._quick_select(nums, 0, len(nums) - 1, k)

def _quick_select(self, nums, left, right, k):
    pivot_idx = random.randint(left, right)
    nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]  # 随机换到最后
    pivot = nums[right]

    lt = left
    eq = left
    for j in range(left, right):
        if nums[j] > pivot:
            nums[j], nums[eq] = nums[eq], nums[j]
            # 遇到大的先放到相等区的最右边 eq 处
            nums[eq], nums[lt] = nums[lt], nums[eq]
            # 与大数区最右边处的 lt 交换
            # 这样 lt 的左边全是大数，eq 的左边全是等于 pivot 的，剩下的就是小于 pivot 的
            lt += 1
            eq += 1
        elif nums[j] == pivot:
            nums[j], nums[eq] = nums[eq], nums[j]
            eq += 1
    nums[eq], nums[right] = nums[right], nums[eq]
    # 遍历完后 pivot 放到相等分区处
    eq += 1  # eq 指向小区开头

    if k <= lt - left:  # 落在大区
        return self._quick_select(nums, left, lt - 1, k)
    elif k <= eq - left:
        # 不管落在相等区的哪个位置，直接返回 pivot
        return pivot
    else:  # 落在小区
        return self._quick_select(nums, eq, right, k - (eq - left))
        # 下次找的 k 为这次的 k 减去 eq 之前的长度，这个长度就是 eq 所在的位置减去 left
```
提交通过，终于从那个测试用例中解脱。现在等于区的元素不会再被递归了。
时间复杂度平均 O(n)：每层遍历 [left, right] 区间，下一层要么去大区、要么去小区（等于区直接返回）。每层区间至少缩减等于区的长度，期望每次剔除约 1/3 的元素，n + 2n/3 + 4n/9 + ... ≈ 3n。极端降序无重复时，每次也只能排除 pivot 自己，退化 O(n²)。
空间复杂度平均 O(log n)——递归栈深度，最坏情况为极端降序且随机化失效时为 O(n)。

## 其他思路

官方的题解中使用的也是类似的方法。
在看题解的时候看到了一个很有趣的题友，他根据题目中 -10⁴ ≤ nums[i] ≤ 10⁴ 的条件创建出了 20001 个桶，然后从上往下累计个数，累计元素数量终于超过了要找的第 K 个，当前值就是答案。
网友的脑洞还真是大，在针对这道题的算法中，他的方法可谓一骑绝尘。可惜不够通用，值域再大几个量级的话就不太适用了。


## 总结

真是一场酣畅淋漓的算法之旅，做得我汗流浃背。

早上打开 LeetCode 看到题目字挺少，准备随便刷刷练练手感，结果越做越不对劲，直接搞到了下午。果然数学里字越少的题目越不简单。

没想到还会用到递归，这是我最薄弱的地方。还有给下一次递归传 k 的地方也是绕了我大概两小时，现在也不敢说是完全理解。

有 AI 真好。曾经大学的时候打开 LeetCode，看完题目就头痛欲裂无从下手，现在直接 AI 搭建好测试用例，专心写算法就行了。一时想不起的语法它也能给你提示，不懂的地方可以刨根问底，还能对比多种语言的不同。

收获颇丰，对复杂度的计算了解得更清晰了，对以前一知半解的快速排序也有了一些了解。堆方法和网友桶排序方法的思路也相当不错。

还是得学习一门后端语言。以前想用 JS 来学算法，堆、链表等结构需要自己构建，本来就不清晰的脑瓜更是感觉到痛苦。Java 我也偶尔写写，但是感觉太累了。

大家说的果然不错：人生苦短，我用 Python。

"""
