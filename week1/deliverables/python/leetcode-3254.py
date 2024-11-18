# Problem Name: 3254. Find the Power of K-Size Subarrays I
# Submission ID: https://leetcode.com/submissions/detail/1454645610/
class Solution:
    def resultsArray(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        ans = [0] * (n - k + 1)
        for i in range(n - k + 1):
            sub = nums[i : i + k]
            is_sorted = True
            for j in range(1, len(sub)):
                if sub[j] - sub[j - 1] != 1:
                    is_sorted = False
                    break

            ans[i] = sub[-1] if is_sorted else -1

        return ans
