import math

def minEatingSpeed(self, piles: List[int], h: int) -> int:
    right = max(piles)
    left = 1
    solution = right

    while left <= right:
        mid = (left + right) // 2
        hours_taken = 0
        for pile in piles:
            hours_taken += math.ceil(pile/mid)
        if hours_taken < h:
            right = mid - 1
        elif hours_taken > h:
            left = mid + 1
        else:
            solution = mid
            right = mid - 1
    return solution