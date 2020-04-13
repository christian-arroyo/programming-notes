def selection_sort(array):
    n = len(array)
    for i in range(n):
        min = i
        for j in range(i+2, n):
            if array[j] < array[min]:
                min = j
        # Swap
        array[i], array[min] = array[min], array[i]
    return array

l = [3,2,8,4,5,6,1]
print(selection_sort(l))
