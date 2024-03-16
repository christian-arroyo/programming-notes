def quick_sort(arr):
    # Helper function for partitioning
    def lomuto_partition(arr, low, high):
        pivot = arr[high]  # Choose the last element as pivot
        i = low - 1  # Index of smaller element

        for j in range(low, high):
            if arr[j] <= pivot:
                # Swap arr[i] and arr[j]
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        # Swap arr[i+1] and arr[high] (pivot)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    # Main quicksort function
    def _quick_sort(arr, low, high):
        if low < high:
            pivot_index = lomuto_partition(arr, low, high)
            _quick_sort(arr, low, pivot_index - 1)
            _quick_sort(arr, pivot_index + 1, high)

    _quick_sort(arr, 0, len(arr) - 1)
    return arr

# Example usage:
arr = [6, 2, 8, 5, 3, 9, 1]
sorted_arr = quick_sort(arr)
print("Sorted array:", sorted_arr)
