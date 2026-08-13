class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = dict()
        for i, item in enumerate(nums):
            x = target - item
            if x in seen:
                return [seen[x], i]
            else:
                seen[item] = i


if __name__ == "__main__":
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1], "标准例子"),
        ([3, 2, 4], 6, [1, 2], "非首位答案"),
        ([3, 3], 6, [0, 1], "两个相同元素"),
        ([1, 2, 3], 5, [1, 2], "简单例子"),
    ]

    sol = Solution()
    for nums, target, expected, desc in test_cases:
        output = sol.twoSum(nums, target)
        print(f"输入: {nums}, target={target}")
        print(f"期望: {expected}, 实际: {output}")
        print(f"描述: {desc}")
        print("-" * 40)

"""
最近心血来潮准备刷完 [LeetCode 热题 HOT 100](https://leetcode.cn/problem-list/2cktkvj/)。

先来一个简单题热热身：[两数之和](https://leetcode.cn/problems/two-sum/description/)

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出和为目标值 `target` 的那两个整数，并返回它们的数组下标。你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。你可以按任意顺序返回答案。

看到这个题一般会想到双重遍历，两两组合等于 `target` 就返回下标。但是这样太不够优雅。

我们只需要把遍历过的数放到字典中，将它作为 `key`、它的下标作为 `value`。后面遍历的数中，如果在字典里有与它加起来能等于 `target` 的数，直接返回两者的下标即可。

```python
def twoSum(self, nums: list[int], target: int) -> list[int]:
    seen = dict()
    for i, item in enumerate(nums):
        x = target - item
        if x in seen:
            return [seen[x], i]
        else:
            seen[item] = i
```

时间复杂度 $O(n)$，空间复杂度最坏情况下要存下 `n - 1` 个数，所以也是 $O(n)$。
"""
