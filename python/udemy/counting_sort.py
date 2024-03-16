def counting_sort(arr):
    # Find the maximum and minimum elements in the array
    max_element = max(arr)
    min_element = min(arr)
    
    # Find the range of the input
    range_of_input = max_element - min_element + 1
    
    # Create a counting array to store the count of each element
    count = [0] * range_of_input
    
    # Count the occurrences of each element in the input array
    for num in arr:
        count[num - min_element] += 1
    
    # Update the counting array to store the position of each element
    for i in range(1, range_of_input):
        count[i] += count[i - 1]
    
    # Create a result array to store the sorted elements
    result = [0] * len(arr)
    
    # Place the elements in their correct positions in the result array
    for num in reversed(arr):
        result[count[num - min_element] - 1] = num
        count[num - min_element] -= 1
    
    return result

# Example usage
arr = [4, -2, 2, -8, 3, 3, -1]
sorted_arr = counting_sort(arr)
print("Sorted array:", sorted_arr)
