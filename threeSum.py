class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        result = []
        nums = sorted(nums)

        for i, a in enumerate(nums):
            if i > 0 and a == nums[i - 1]:
                continue

            j, k = i + 1, len(nums) - 1
            while j < k:
                s = a + nums[j] + nums[k]
                if s == 0:
                    result.append([a, nums[j], nums[k]])
                    j += 1
                    k -= 1
                    while j < k and nums[j] == nums[j - 1]:
                        j += 1
                    while j < k and nums[k] == nums[k + 1]:
                        k -= 1

                    # 这一步相当于去重
                elif s < 0:
                    j += 1
                else:
                    k -= 1

        return result


if __name__ == "__main__":
    test_cases = [
        ([0, 0, 0, 0], "全零数组"),
        ([1, 2, -3, 4, -1], "包含一组解"),
        ([1, 2, 3, 4, 5], "无解"),
        ([-1, 0, 1, 2, -1, -4], "多组解，含重复元素"),
        ([-1, 0, 1, 2, -4], "多组解，含重复元素"),  # 不可重复使用其中的某一个元素
        ([-1, 0, 1, 0], "多组解，含重复元素"),
        ([1, 2, 0, 1, 0, 0, 0, 0], "多组解，含重复元素"),
        ([-2, 0, 1, 1, 2], "多组解，含重复元素"),
    ]

    sol = Solution()
    for nums, desc in test_cases:
        output = sol.threeSum(nums)
        print(f"输入: {nums}")
        print(f"描述: {desc}")
        print(f"输出: {output}")
        print("-" * 40)


"""
最近在学python，研究个算法来练练手：三数之和。

看题目我想出了两种思路：

思路1：列出所有可能的三元组，去重，计算和是否为0。比较暴力，可能的组合太多，消耗太大。
思路2：两两组合求和，再在剩余的数组中看是否有能加起来为0的项，消耗也不少，但是先试试。
实操过程
双层遍历两两组合，使用enumerate拿到索引后，内部循环使用切片来避免重复组合。nums[i + 1 :]表示从索引i的下一个位置开始到数组末尾的所有元素。

Copy
for i, a in enumerate(nums):
    for b in nums[i + 1 :]:
        pass
下一步是在数组nums中寻找是否存在一个元素c，使得a + b + c = 0，即c = -(a + b)。使用的是if c in nums。但是遇到了两个问题：

c可能是a或b本身，导致重复使用同一个元素。于是采用nums.count(c)来判断c在nums中出现的次数是否足够。如果只有一个出现次数，而c正好是a或b，那么就不能使用。
如果a == b == c == 0，那么就需要至少三个0才能组成一个三元组。
找到c后，使用sorted([a, b, c])来对三元组进行排序，然后加入result中，后续判断result中数组中是否有相同数组，有的话就不加入，达到去重的目的。

Copy
def threeSum(self, nums: list[int]) -> list[list[int]]:
    result = []
    for i, a in enumerate(nums):
        for b in nums[i + 1:]:
            c = -(a + b)
            if c not in nums:
                continue

            if c == a and a == b:
                if nums.count(a) < 3:
                    continue
            elif c == a or c == b:
                if nums.count(c) < 2:
                    continue

            triplet = sorted([a, b, c])
            if triplet not in result:
                result.append(triplet)

    return result
加上了这些判断后运行，测试用例通过，自信满满点了提交，结果遇到了一个超长的数组，直接超时了。看来这个思路也不行，还得需要更节省性能的方法。

算法优化
在ai的提示下修改了一下思路：采用排序加双指针的方法。

首先排序整个数组，然后遍历数组，在剩下的数组元素中的两端各放一个指针，相加三个数。 如果这个数大于0，说明需要减小这个数，右指针左移； 如果小于0，说明需要增大这个数，左指针右移； 如果等于0，说明找到了一个解，加入结果中，并且左右指针都移动一位。

Copy
def threeSum(self, nums: list[int]) -> list[list[int]]:
    result = []
    nums = sorted(nums)

    for i, a in enumerate(nums):
        if i > 0 and a == nums[i - 1]:
            continue

        j, k = i + 1, len(nums) - 1
        while j < k:
            s = a + nums[j] + nums[k]
            if s == 0:
                result.append([a, nums[j], nums[k]])
                j += 1
                k -= 1
                while j < k and nums[j] == nums[j - 1]:
                    j += 1
                while j < k and nums[k] == nums[k + 1]:
                    k -= 1

                # 这一步相当于去重
            elif s < 0:
                j += 1
            else:
                k -= 1

    return result
在等于0的情况下，为了避免重复解，使用while循环持续移动指针跳过相同的元素，保证不会出现重复解。

移动指针时 while nums[j] == nums[j-1] 是往后看（刚用过的值），不能往前看，否则会跳过没处理的解。

原本在elif和else中也使用了while循环来跳过相同的元素，但是发现这样会漏掉一些解，并且增加代码了复杂度。虽然理论上能减少几轮循环，但收益极小，不值当。

这个方法对比之前方法的巧妙之处在于：

之前在外层固定 a，然后还需要第二层循环 b，再去数组里线性找 c，找两数的过程是 O(n²) × O(n) = O(n³)。现在排序后，数组是有序的。j 在最左（最小），k 在最右（最大），比较一次就能决定谁移动：和太小就右移 j（变大），和太大就左移 k（变小）。每轮只动一个指针，两个指针相聚一次就走了完所有可能的 (b, c) 组合，只是一趟 O(n)，极大减少了时间复杂度。
去重变成了顺带的事，排序后相同值挤在一起，跳过重复只需要看相邻元素是否相等。你之前得先 sorted(triplet) 转成标准形式再 not in result 逐次查重，那是边跑边踩刹车，这也极大的减小了性能的开销。
其他思路
还可以使用哈希表的方法，和我第一次思考的方法有点相似，不过它将c的结果(0-(a+b))存储到了map中，下次寻找的时候就不用在从数组中线性寻找c，减少了O(n)的时间复杂度。 缺点也是缺点是去重麻烦——得用 set 手动去重或借助排序。

实际上 O(n²) 是这道题的已知最优时间复杂度（一般公认），双指针和哈希表都是 O(n²)，双指针胜在空间 O(1) 且去重天然顺手，所以是主流写法。

总结
在数组中找一个数的时候不要遍历数组，而是优先使用哈希表：c in nums（O(n)）vs c in set（O(1)）。
移动指针O(n)比遍历两次数组O(n²)来配对能够节省很多性能。
排序的复杂度很低（Python 的 sorted() 使用的是 Timsort——一种混合了归并排序和插入排序的稳定排序算法，由 Tim Peters 在 2002 年为 Python 设计。它特别擅长处理现实中常见的"部分有序"数据，最优情况 O(n)，最坏 O(n log n)。Java 和 Android 的默认排序后来也采用了 Timsort。）

"""
