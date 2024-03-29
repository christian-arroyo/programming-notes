from typing import List
def productExceptSelf(nums: List[int]) -> List[int]:
        prefix = nums.copy()
        postfix = nums.copy()
        prefix[0] = 1
        postfix[-1] = 1
        solution = []
        for i in range(len(prefix) - 1):
            prefix[i+1] = nums[i] * prefix[i]

        for i in range(len(postfix) -1, 0, -1):
            postfix[i-1] = nums[i] * postfix[i]

        for i in range(len(nums)):
            solution.append(prefix[i] * postfix[i])
        return solution

nums = [1,2,3,4]
print(productExceptSelf(nums))
