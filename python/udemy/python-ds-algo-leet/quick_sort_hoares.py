def quick_sort(arr):
    # Helper function for partitioning
    def hoare_partition(arr, low, high):
        pivot = arr[low]  # Choose the first element as pivot
        i = low - 1
        j = high + 1

        while True:
            i += 1
            while arr[i] < pivot:
                i += 1

            j -= 1
            while arr[j] > pivot:
                j -= 1

            if i >= j:
                return j

            arr[i], arr[j] = arr[j], arr[i]

    # Main quicksort function
    def _quick_sort(arr, low, high):
        if low < high:
            pivot_index = hoare_partition(arr, low, high)
            _quick_sort(arr, low, pivot_index)
            _quick_sort(arr, pivot_index + 1, high)

    _quick_sort(arr, 0, len(arr) - 1)
    return arr

# Example usage:
arr = [6, 2, 8, 5, 3, 9, 1]
sorted_arr = quick_sort(arr)
print("Sorted array:", sorted_arr)
