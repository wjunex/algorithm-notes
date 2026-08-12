class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {
            "{": "}",
            "(": ")",
            "[": "]",
        }
        stack = []
        for ch in s:
            if ch in pairs:
                stack.append(ch)
            else:
                if not stack or pairs[stack.pop()] != ch:
                    return False
        return not stack


if __name__ == "__main__":
    test_cases = [
        ("()", True, "一对括号"),
        ("()[]{}", True, "多种括号"),
        ("(]", False, "不匹配"),
        ("([)]", False, "交叉嵌套"),
        ("{[]}", True, "正确嵌套"),
        ("", True, "空字符串"),
        ("(", False, "单个左括号"),
        ("]", False, "单个右括号"),
    ]

    sol = Solution()
    for s, expected, desc in test_cases:
        output = sol.isValid(s)
        print(f"输入: '{s}'")
        print(f"期望: {expected}, 实际: {output}")
        print(f"描述: {desc}")
        print("-" * 40)

"""
继续研究：[有效的括号](https://leetcode.cn/problems/valid-parentheses/description/)

给定一个只包括 `'('`、`')'`、`'{'`、`'}'`、`'['`、`']'` 的字符串 `s`，判断字符串是否有效。
有效字符串需满足：左括号必须用相同类型的右括号闭合，左括号必须以正确的顺序闭合，每个右括号都有一个对应的相同类型的左括号。

这道题我曾经做过几次，思路基本上是用栈后进先出的特性来解决。

遇到左括号，压入栈中。遇到右括号，看与栈顶左括号能否匹配上，能匹配则弹出栈顶；与栈顶不匹配直接返回 `False`。一一匹配完后看栈中是否还有剩余左括号，有的话也返回 `False`。

```python
def isValid(self, s: str) -> bool:
    pairs = {
        "{": "}",
        "(": ")",
        "[": "]",
    }
    stack = []
    for ch in s:
        if ch in pairs:
            stack.append(ch)
        else:
            if not stack or pairs[stack.pop()] != ch:
                return False
    return not stack
```
$O(n)$ 时间、$O(n)$ 空间。每个字符最多进栈一次、出栈一次，一趟遍历完成。最坏情况（全是左括号）栈存 `n` 个字符。

还有一个思路也值得参考：就是不断地消除字符串中匹配的 `()`、`[]`、`{}`，将其替换成空字符串，直到没有能够匹配的括号，观察剩余的字符串是否被消除干净。

```python
while "()" in s or "[]" in s or "{}" in s:
    s = s.replace("()", "").replace("[]", "").replace("{}", "")
return s == ""
```

时间复杂度最坏为 $O(n^2)$——括号层层嵌套时每一层都要扫一遍字符串。
"""
