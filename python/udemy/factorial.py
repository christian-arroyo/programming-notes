# Factorial = n * n!
def find_factorial_recursive(number):
    if number == 1:
        return 1
    answer = number * find_factorial_recursive(number - 1)
    return answer


def find_factorial_iterative(number):
    answer = 1
    for i in range(1, number+1):
        answer = answer * i
    return answer

print(find_factorial_recursive(5))
print(find_factorial_iterative(5))
