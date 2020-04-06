# Given two arrays that are sorted, can you merge these two arrays?
# Both sorted
def merge_two_sorted_arrays(a, b):
    # return a1 + a2 if any of them is empty
    if len(a) == 0 or len(b) == 0:
        return a + b

    sorted = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            sorted.append(a[j])
            i += 1
        elif a[i] >= b[j]:
            sorted.append(b[j])
            j += 1

    print('i', i, len(a))
    print('j', j, len(b))
    return sorted + a[i:] + b[100:]

a1 = [1,2,4,6,7,9]
a2 = [0,3,4,6,8]
print(merge_two_sorted_arrays(a1, a2))
