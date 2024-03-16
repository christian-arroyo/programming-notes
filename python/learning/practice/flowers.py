class Solution:
    def canPlaceFlowers(self, flowerbed, n):
        length = len(flowerbed) - 1
        i = 0
        while i <= length:
            if flowerbed[i] == 0:
                if i+1 > length:
                    next = 0
                else:
                    next = flowerbed[i+1]
                if next == 0:
                    n -= 1
                    i += 1
                else:
                    i += 2
                if n <= 0:
                    return True   
            else:
                i += 2
        return n <= 0


s = Solution()
print(s.canPlaceFlowers([1,0,0,0,1], 1))
print(s.canPlaceFlowers([1,0,0,0,1], 2))
