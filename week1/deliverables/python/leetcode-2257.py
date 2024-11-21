# Problem Name: 2257. Count Unguarded Cells in the Grid
# Submission ID: https://leetcode.com/problems/count-unguarded-cells-in-the-grid/submissions/1459311418

class Solution:
    def countUnguarded(self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]) -> int:
        ans = 0
        g = set()
        w = set()
        visited = set()

        for r, c in walls:
            w.add((r,c))

        for r, c in guards:
            g.add((r, c))
        
        def is_valid(r, c):
            return 0 <= r < m and 0 <= c < n and (r, c) not in g and (r, c) not in w

        total_guraded = len(guards) + len(walls)
        for i, j in guards:
            # north
            for r in range(i-1, -1, -1):
                if not is_valid(r, j):
                    break
                if  (r, j) not in  visited:
                    visited.add((r, j))
                    total_guraded += 1
           
            for c in range(j+1, n):
                if not is_valid(i, c):
                    break
                if (i, c) not in  visited:
                    visited.add((i, c))
                    total_guraded += 1
            
            for r in range(i+1, m):
                if not is_valid(r, j):
                    break
                if (r, j) not in  visited:
                    visited.add((r, j))
                    total_guraded += 1
            
            for c in range(j - 1, -1, -1):
                if not is_valid(i, c):
                    break
                if (i, c) not in  visited:
                    visited.add((i, c))
                    total_guraded += 1

        return n * m - total_guraded
