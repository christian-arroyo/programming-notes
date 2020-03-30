# 1 1 2 3 5 8
# f(n) = f(n-1) + f(n-2) if n >= 3
# F(n) = 1 if n=1 or 2

def fib(n):
    if n == 2 or n ==1: # base case
        return 1
    elif n >= 3:
        fibonacci = fib(n-1) + fib(n-2)
    return fibonacci

# print(fib(1))
# print(fib(2))
# print(fib(3))
# print(fib(35))


# 1 1 2 3 5 8 13 ... n O(n)
def fib_dynamic(n, memo):
    # return element of array if it already exists
    if memo[n] is not None:
        return memo[n]
    if n == 1 or n == 2:
        memo[n] = 1
    else:
        memo[n] = fib_dynamic(n-1, memo) + fib_dynamic(n-2, memo)
    return memo[n]

n = 5
memo = [None] * (n + 1)
print(fib_dynamic(n, memo))

def fib_bottom_up(n):
    if n == 1 or n == 2:
        return 1
    bottom_up = [None] * (n + 1)
    bottom_up[1] = 1
    bottom_up[2] = 1
    for i in range(3, n + 1):
        bottom_up[i] = bottom_up[i-1] + bottom_up[i-2]
    return bottom_up[n]

print(fib_bottom_up(5))
