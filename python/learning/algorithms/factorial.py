# factorial = n * n-1 * n-2 ... 2 * 1 for n >= 1
# if n == 0 then return 1 as 0! = 1

def fact(n):
    # Assuming n is a positive integer or 0
    if n == 0:
        return 1
    else:
        factorial = n * fact(n-1)
    return factorial


print(fact(4))
