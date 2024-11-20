# Problem Name: 2516. Take K of Each Character From Left and Right
# Submission ID: https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/submissions/1458318106

class Solution:
    def takeCharacters(self, s: str, k: int) -> int:
        freq = Counter(s)

        def is_valid_window(d):
            for c in ['a', 'b', 'c']:
                if freq[c] - d[c] < k:
                    return False
            return True
        
        l = 0
        cur_window_freq = defaultdict(int)
        largest_window = 0
        for r in range(len(s)):
            cur_window_freq[s[r]] += 1
            while l < len(s) and not is_valid_window(cur_window_freq):
                cur_window_freq[s[l]] -= 1
                l += 1
            largest_window = max(largest_window, r - l + 1)

        return  (len(s) - largest_window) if is_valid_window(cur_window_freq) else -1
            
