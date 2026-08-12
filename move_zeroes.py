class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        i = 0

        for item in nums:
            if item != 0:
                nums[i] = item
                i += 1

        while i < len(nums):
            nums[i] = 0
            i += 1


if __name__ == "__main__":
    test_cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0], "标准例子"),
        ([0], [0], "单个零"),
        ([1], [1], "无零"),
        ([2, 1], [2, 1], "无零"),
        ([0, 0, 1], [1, 0, 0], "连续零"),
        ([1, 0, 2, 0, 3], [1, 2, 3, 0, 0], "交替零"),
    ]

    sol = Solution()
    for nums, expected, desc in test_cases:
        original = nums.copy()
        sol.moveZeroes(nums)
        print(f"输入: {original}")
        print(f"期望: {expected}, 实际: {nums}")
        print(f"描述: {desc}")
        print("-" * 40)

"""
继续尝试：[移动零](https://leetcode.cn/problems/move-zeroes/description/)

给定一个数组 `nums`，编写一个函数将所有 `0` 移动到数组的末尾，同时保持非零元素的相对顺序。请注意，必须在不复制数组的情况下原地对数组进行操作。

一开始读题，想把所有 `0` 移动到数组的末尾，发现不好处理非零数的顺序。转念一想，将所有非零数移动到数组前面，剩下的不就都是 `0` 了吗。

## 双指针交换法

想到前面快速选择中有用到一个方法：将大于基点的数移动到基点左边，小于基点的数放在基点右边。在这里我们把 `0` 看作基点，就能直接得出这道题的答案了。

```python
def moveZeroes(self, nums: list[int]) -> None:
    i = 0
    for j in range(len(nums)):
        if nums[j] != 0:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
```
`i` 始终指向"下一个非零元素应该放的位置"，`j` 遍历数组。遇到非零就交换，`i` 前移。时间复杂度 $O(n)$，空间 $O(1)$。

## 覆写 + 补零法

还有一个简单而有趣的思路：遍历数组的时候，将所有的非零数用来覆盖掉数组的前半段，然后将数组剩下的部分全部用 `0` 来覆盖即可。

```python
def moveZeroes(self, nums: list[int]) -> None:
    i = 0

    for item in nums:
        if item != 0:
            nums[i] = item
            i += 1

    while i < len(nums):
        nums[i] = 0
        i += 1
```
时间复杂度 $O(n)$，空间 $O(1)$。

虽然两者的时间复杂度都是 $O(n)$，实际执行起来覆盖法比交换法更快。因为 swap 每次要三步——`a` 存临时、`b` 给 `a`、临时给 `b`。Python 的 `a, b = b, a` 背后是元组打包再拆包，有额外开销。

覆盖法只做一步赋值 `nums[i] = item`，元素直接落位。零也只补一次，不是每次换都带着零。

所以虽然都是 $O(n)$，覆盖法的常数更小。非零越多、交换越频繁时差距越明显。

"""
