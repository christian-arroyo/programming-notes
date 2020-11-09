def fibonacci(n):
    array = [None] * (n+1)
    return _fibonacci(n, array)

def _fibonacci(n, array):
    # 1 1 2 3 5 8 13 21
    # If item exists in array, return it
    if array[n]:
        return array[n]
    if n == 0:
        array[0] = 0
    elif n == 1 or n == 2:
        array[n] = 1
    else:
        array[n] = _fibonacci(n-1, array) + _fibonacci(n-2, array)
    return array[n]


print(fibonacci(1))
