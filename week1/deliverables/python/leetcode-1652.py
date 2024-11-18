# Problem Name: Defuse the Bomb
# Submission ID: https://leetcode.com/submissions/detail/1456310208/
class Solution:
    def decrypt(self, code: List[int], k: int) -> List[int]:
        circular = code + code
        n = len(code)
        ans = [0] * n

        for i in range(n):
            if k == 0:
                ans[i] = 0

            elif k > 0:
                start = (i + 1) % n
                ans[i] = sum(circular[start : start + k])

            else:
                start = i + n - abs(k)
                ans[i] = sum(circular[start : start + abs(k)])

        return ans
