from typing import List

def topKFrequent(nums: List[int], k: int) -> List[int]:
    map_count = {}
    count_list = [[] for _ in range(len(nums) + 1)]
    solution = []
    # Count values into hash map
    for num in nums:
        if num not in map_count:
            map_count[num] = 1
        else:
            map_count[num] += 1
    for number, count in map_count.items():
        count_list[count].append(number)

    index = len(count_list) - 1
    while k > 0:
        if count_list[index]:
            solution.append(count_list[index].pop())
            k -= 1
        else:
            index -= 1
    return solution

lst = [1,1,1,2,2,3]
print(topKFrequent(lst, 2))

