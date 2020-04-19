# Given a numnber n, return the index value of the Fibonacci sequence
# answer = [n-2] + [n-1] .. 1 + 0


def fib_iterative(n):
    answers = [0, 1]
    for i in range(2, n+1):
        answers.append(answers[i-2] + answers[i-1])
    return answers[n]
    if n <= 1:
        return 1

# Slow O(n^2)
def fib_recursive(n):
    if n < 2:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)

# Fast, O(n)
def fib_recursive_dynamic(n, cache):
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    else:
        cache[n] = fib_recursive_dynamic(n-1, cache) + fib_recursive_dynamic(n-2, cache)
        return cache[n]


# print(fib_iterative(10))
print(fib_recursive(20))
print(fib_recursive_dynamic(20, {}))
