def bubble_sort(array):
    n = len(array)
    for i in range(n):
        for j in range(n-1-i):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    return array

a = [3, 5, 76, 8, 9, 1, 7]
print(bubble_sort(a))
