class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        answer = [0] * len(temperatures)
        for i in range(len(temperatures) - 2, -1, -1):
            j = i + 1  # 初始化j，为当前数的后一项
            while (
                j < len(temperatures)  # j在范围内
                and answer[j] > 0  # 后面还有比temperatures[j]大的数
                and temperatures[j] <= temperatures[i]  # 当前的j的数不满足条件
            ):
                j += answer[j]  # 将j跳到下一个大数

            if temperatures[j] > temperatures[i]:
                answer[i] = j - i

        return answer


if __name__ == "__main__":
    test_cases = [
        ([73, 74, 75, 71, 69, 72, 76, 73], "标准例子"),
        ([30, 40, 50, 60], "持续升温"),
        ([30, 60, 90], "持续升温，等长递减"),
        ([90, 60, 30], "持续降温，无升温日"),
    ]

    sol = Solution()
    for temps, desc in test_cases:
        output = sol.dailyTemperatures(temps)
        print(f"温度: {temps}")
        print(f"描述: {desc}")
        print(f"输出: {output}")
        print("-" * 40)

"""
今天继续研究算法：每日温度https://leetcode.cn/problems/daily-temperatures/description/

给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。

一读题目感觉很简单，就只用操作一个数组，但是想优雅的完成，还是需要耗费一点脑细胞。

先写个暴力破解进入状态：
```python
def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
    answer = []
    for i, item1 in enumerate(temperatures):
        answer.append(0)
        for j, item2 in enumerate(temperatures[i + 1 :]):
            if item2 > item1:
                answer[i] = j + 1 # 加一是将下标转变成间隔的天数，比如第二天就符合要求，那么j是0，加一变成间隔一天
                break # 找到第一个符合条件的就退出循环

    return answer
```
时间复杂度是 O(n²) （n²/2，大 O 里常数 1/2 被忽略）。

又遇到双层遍历，看看能不能用哈希表，在这个题目中好像不太适用。

苦思之下找不到好的办法，在AI的提示下得到一个思路：

既然是找当前数的下一个比它大的数，那么我们就在找到之前将它连同它的下标压入一个栈中。
轮询到下一个数的时候，将它与栈顶进行对比，如果当前数比栈顶的要大，那么这个数就是我们要找的。现在将栈顶出栈，栈顶到目前数的距离就是当前数的下标减去它的下标。此时我们将answer和它相同下标的位置设置成下标之差即可。
如果当前数比栈顶数小，那么将其压入栈顶，静静等待它的下一个比它大的数。如果来了一个非常大的数，就将栈中所有比它小的数出栈并记录位置。这样如果没有比栈中的数更大的数的话，它们就在栈中不出来，也不设置answer的值，默认为0说明后面没有比它更大的数了。

稍微有点抽象，AI给出我这个思路的时候我也是思考了很久，说白了就是一句话：记录下当前的下标，当后面第一个比它大的数出现的时候计算两个数之间的距离。只是过程中利用到了栈的一些特性（单调递减栈），使用set/dict是没办法做到的（set/dict 无序）。
这个方法的时间复杂度为O(n)，因为每个元素最多入栈出栈各一次（while迭代的次数也不会超过n次，复杂度为 O(2n)，常数省略即为 O(n)）。不过空间复杂度来到了O(n)，栈最坏的情况下要存全部元素。

```python
def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack = []
    for index, item in enumerate(temperatures): # 遍历一遍
        while stack and item > stack[-1][1]: 
            i, _ = stack.pop() # 栈中比当前小的统统出栈
            answer[i] = index - i # 记录距离
        stack.append((index, item)) # 当前数进栈
    return answer
```


除此之外，还有一个巧妙的方法：
从列表的后面往前计算，将计算的结果放在answer中。再计算前面一个，如果这个数的下一项的数没有它大，那么之间跳过无效的比较，直接比较它下一项的数最近的最大的那个数（已经知道结果）。如果这个数还是没它大，继续比较下一个结果，都没有那么它的结果就是0。
这个方法能省下栈的空间，空间复杂度降低到了O(1)。

"""
