# Given an array, find first recurring number

# ist it sorted?
# negative values?
# small or large input?

# O(n^2)
# def recurring_number(array):
#     i = 0
#     while i < len(array):
#         j = i + 1
#         while j < len(array):
#             if array[j] == array[i]:
#                 return array[j]
#             j += 1
#         i += 1
#     return False

# O(n)
def recurring_number2(array):
    my_dict = dict()

    for n in array:
        if n in my_dict.keys():
            return n
        my_dict[n] = 1
    return False

array1 = [1, 2, 5, 6, 9, 4, 5, 3, 6]
print(recurring_number2(array1))
