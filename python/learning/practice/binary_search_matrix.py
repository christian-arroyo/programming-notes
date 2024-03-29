from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        row_with_possible_match = self.binary_search_rows(matrix, target)
        print(row_with_possible_match)
        if not row_with_possible_match:
            return False
        else:
            return self.binary_search(row_with_possible_match, target)
    
    def binary_search_rows(self, matrix, target) -> list:
        start = 0
        end = len(matrix) - 1
        while start <= end:
            mid = (start + end) // 2
            if target < matrix[mid][0]:
                end = mid - 1
            elif target > matrix[mid][-1]:
                start = mid + 1
            else:
                return matrix[mid]
        return []
                  
    
    def binary_search(self, array, target) -> int:
        start = 0
        end = len(array) - 1
        while start <= end:
            mid = (start + end) // 2
            if target < array[mid]:
                end = mid - 1
            elif target > array[mid]:
                start = mid + 1
            else:
                return True
        return False

s = Solution()
m = [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
target = 3 
print(s.searchMatrix(m, target))
