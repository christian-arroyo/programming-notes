def insertion_sort(arr):

    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >=0 and key < arr[j] :
                arr[j+1] = arr[j]
                j -= 1
        # Write small value in its place
        arr[j+1] = key
    return arr

l = [3,5,7,1,6,2,9]
print(insertion_sort(l))
