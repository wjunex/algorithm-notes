class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        dist = {}
        for item in strs:
            count = [0] * 26
            for ch in item:
                # ord(ch) 返回字符的 Unicode 码点。ord('a') = 97，ord('a') - 97 = 0，ord('z') - 97 = 25——把字母映射到 0~25 的数组下标
                count[ord(ch) - 97] += 1
            # tuple(count) 把列表转成元组。列表不可哈希，不能做字典 key；元组不可变、可哈希，能做 key。
            key = tuple(count)
            if key in dist:
                dist[key].append(item)
            else:
                dist[key] = [item]
        return list(dist.values())


if __name__ == "__main__":
    test_cases = [
        (["eat", "tea", "tan", "ate", "nat", "bat"], "标准例子"),
        ([""], "单个空字符串"),
        (["a"], "单个字母"),
        (["", ""], "两个空字符串"),
    ]

    sol = Solution()
    for strs, desc in test_cases:
        output = sol.groupAnagrams(strs)
        print(f"输入: {strs}")
        print(f"描述: {desc}")
        print(f"输出: {output}")
        print("-" * 40)

"""
今天研究：[字母异位词分组](https://leetcode.cn/problems/group-anagrams/description)
给你一个字符串数组，请你将字母异位词组合在一起。可以按任意顺序返回结果列表。

读题发现，就是说两个词的字母相同，但是顺序不同，一个词可以通过调整字母顺序变成另一个词，这两个就是字母异位词。
理论上来说，遍历一遍数组，将元素一个个归类就行，难点在于如何知道两个词是异位词。

## 排序法

我首先的想法是将字符串排序，异位词经过排序后就变成了相同的词。然后将排序后的字符串作为 `key` 放到字典中归类，最后返回列表即可。

```python
def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
    dist = {}
    for item in strs:
        key = "".join(sorted(item))  # 排序
        if key in dist:
            dist[key].append(item)
        else:
            dist[key] = [item]
    return list(dist.values())
```
时间复杂度：`n` 个字符串，每个排序 $O(k \log k)$，总计 $O(nk \log k)$。
空间 $O(nk)$。

## 计数法

优化一下，用一个长度为 `26` 的元组作为 `key`，统计每个字母出现次数。异位词的计数数组相同。每个 $O(k)$，省了排序的 $k \log k$，让复杂度降到了 $O(nk)$。

因为这个题限定了只有 `26` 个小写字母，如果是 ASCII 全部可打印字符，则 `count` 开到 `128`。如果完全未知字符集这个方法就不适用了，只能使用上面的排序法或 `Counter`（Python `collections` 里的一个字典子类，专门统计每个元素出现次数，本质上是个自动扩容的哈希计数表）。
```python
def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
    dist = {}
    for item in strs:
        count = [0] * 26
        for ch in item:
            # ord(ch) 返回字符的 Unicode 码点。ord('a') = 97，ord('a') - 97 = 0，ord('z') - 97 = 25——把字母映射到 0~25 的数组下标
            count[ord(ch) - 97] += 1
        # tuple(count) 把列表转成元组。列表不可哈希，不能做字典 key；元组不可变、可哈希，能做 key。
        key = tuple(count)
        if key in dist:
            dist[key].append(item)
        else:
            dist[key] = [item]
    return list(dist.values())
```

还有一个有趣的现象：在 LeetCode 上提交后，排序法执行用时 `11 ms`，而计数法反而来到了 `19 ms`。计数法的时间复杂度不是更小吗，为什么反而用了更多的时间？
原来有两个原因：
- `sorted()` 是 C 实现的。计数法每个字符都要走 Python 层的 `for` 循环 + `ord()` + 数组索引 + 赋值，全是 Python 字节码。`sorted()` 一把推进 C 层跑完，几乎没有 Python 层开销，Python 的 C 层排序比 Python 层循环快太多。
- 力扣的测试用例字符串很短，单词长度就 `3`~`5` 个字母，$k \log k$ 的 $\log$ 几乎可以忽略。C 层秒杀 Python 层的常数差距。计数法在超长字符串（比如几千个字符）才可能反超。

由此我得出一个结论：有时候一味地追求减少算法的时间复杂度并不能达到理想的效果，需要根据客观因素来选择最合适的算法，才能使效率最大化。

没有最好的算法，只有最合适的算法。
"""
