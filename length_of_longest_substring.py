class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        i = 0
        result = 0
        for j, ch in enumerate(s):
            if ch in seen and seen[ch] >= i:
                i = seen[ch] + 1
            seen[ch] = j
            result = max(result, j - i + 1)
        return result


if __name__ == "__main__":
    test_cases = [
        ("abcabcbb", 3, "最长子串 abc"),
        ("bbbbb", 1, "全重复"),
        ("pwwkew", 3, "最长子串 wke"),
        ("", 0, "空字符串"),
        (" ", 1, "单个空格"),
        ("au", 2, "无重复"),
        ("dvdf", 3, "需要移动左边界"),
    ]

    sol = Solution()
    for s, expected, desc in test_cases:
        output = sol.lengthOfLongestSubstring(s)
        print(f"输入: '{s}'")
        print(f"期望: {expected}, 实际: {output}")
        print(f"描述: {desc}")
        print("-" * 40)

"""
继续研究：[无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/description/)

给定一个字符串 `s`，请你找出其中不含有重复字符的最长子串的长度。

首先想到的方法是遍历并将字符压入栈中，遇到已经在栈中存在的元素则记录下栈的长度后清空栈，对字符串中每一个字符都如此操作一遍。

```python
def lengthOfLongestSubstring(self, s: str) -> int:
    result = 0
    stack = []
    for i in range(len(s)):
        for ch in s[i:]:
            if ch not in stack:
                stack.append(ch)
            else:
                break
        result = len(stack) if len(stack) > result else result
        stack.clear()
    return result
```

不出我所料，提交时果然超时了。

时间 $O(n^3)$：外层循环 `n` 次，内层遍历 `s[i:]` 最坏 `n` 次，每次 `ch not in stack` 要线性扫描栈（最坏 `n`），三层相乘。空间 $O(n)$。

优化一下。既然清空栈的时候已经有了一串不重复的字符串，那么轮到下一个元素时，又需要重新累积一串只比它少一个字符的字符串。为什么不直接让前面那个重复的字符离开，保留剩下的无重复子串呢。

由此我想到了用队列来处理。字符依次进队，如果当前准备进队的字符已经在队列中有相同的字符，那么从队头一直出队，直到将与当前元素相同的那个字符释放掉，再将当前字符加入队中。

在进队时不断记录队列的长度，其中最大的数就是我们要找的无重复字符的最长子串的长度。

```python
def lengthOfLongestSubstring(self, s: str) -> int:
    result = 0
    window = deque()
    for item in s:
        if item in window:
            while True:
                x = window.popleft()
                if x == item:
                    break
        window.append(item)
        result = len(window) if len(window) > result else result
    return result
```

时间 $O(n^2)$：`item in window` 每次线性扫描窗口（最坏 `n`），外层遍历 `n` 次。空间 $O(n)$。

瓶颈在 `item in window` 的线性判重，把这一层换成哈希表可以降到 $O(1)$，整体到 $O(n)$。

既然能用队列，理论上用双指针也能达到同样的效果，还能省下队列占的空间。同时把 `item in window` 换成 `set` 来判断。

```python
def lengthOfLongestSubstring(self, s: str) -> int:
    result = 0
    ch_set = set()
    i = 0
    for j in range(len(s)):
        if s[j] in ch_set:
            while True:
                ch_set.remove(s[i])
                if s[i] == s[j]:
                    break
                else:
                    i += 1
            i += 1
        ch_set.add(s[j])
        result = max(result, j - i + 1)
    return result
```

子串长度直接用双指针的距离差 `j - i + 1` 即可。时间 $O(n)$：外层 `for` 走 `n` 次，内层 `while` 里 `i` 只增不减，全程从 `0` 最多走到 `n`，总共执行 `n` 次 `remove`，均摊到每次 $O(1)$。`set` 的 `add`、`remove`、`in` 都是均摊 $O(1)$。

空间 $O(1)$：`ch_set` 最多装下整个窗口，而窗口内字符无重复，长度被字符集大小封顶（字母、数字、符号就几十个），不随 `n` 增长。

虽然解决了问题，但我觉得这个方法不够优雅。Python 里没有 `do-while`，只能用 `while True` 加 `break` 来模拟。每个字符都要先在集合里移除，再看它是不是当前元素的重复值：不是就移动下标继续循环，是的话跳出循环后再把指针后移一位。这样写法上不太优雅，甚至有点丑陋。

还有一个问题：`set` 只回答"这个字符在不在窗口里"，不回答"它在哪个位置"。所以重复时只能从左边一个个删、一个个找。

假如不用 `set` 而用 `dict`，用字符做 `key`、下标做 `value`。这样就不用移除字典里的元素，只需要根据它的 `value` 看下标是否落在当前子串里就行了。

```python
def lengthOfLongestSubstring(self, s: str) -> int:
    seen = {}
    i = 0
    result = 0
    for j, ch in enumerate(s):
        if ch in seen and seen[ch] >= i:
            i = seen[ch] + 1
        seen[ch] = j
        result = max(result, j - i + 1)
    return result
```

这样修改之后看着顺眼多了。巧妙的地方在于，我们能轻易知道重复值的下标，直接把 `i` 移动到它的后面就行了。

也不用把 `i` 跳过的元素从字典里移除——如果字典里某个元素存的下标在 `i` 的前面，它就与当前窗口无关了，直接忽略。

时间 $O(n)$：`for` 走 `n` 次，每轮都是字典 $O(1)$ 操作，没有内层循环。空间 $O(1)$：`seen` 最多装下整个字符集（字母、数字、符号加起来就几十个），不随 `n` 增长。set 版和字典版空间其实一样，字典版真正的优势是省掉了 `while` 逐一出队，时间常数更小、代码更简洁。
"""
