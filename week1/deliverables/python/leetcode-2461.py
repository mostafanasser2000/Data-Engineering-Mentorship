# Problem Name: 2461. Maximum Sum of Distinct Subarrays With Length K
# Submission: https://leetcode.com/submissions/detail/1457318377/

class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        ans = 0
        l = 0
        freq = defaultdict(int)
        cur_sum = 0
        for r in range(len(nums)):
            cur_sum += nums[r]
            freq[nums[r]] += 1
            while freq[nums[r]] > 1:
                cur_sum -= nums[l]
                freq[nums[l]] -= 1
                l += 1
            
            if r - l + 1 == k:
                ans = max(ans, cur_sum)
                cur_sum -= nums[l]
                freq[nums[l]] -= 1
                l += 1

            
        
        return ans
