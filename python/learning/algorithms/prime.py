# Program to identify if a number is prime
import math


# slow
def is_prime(number):
    if number > 1:
        for x in range(2, number):
            if number % x == 0:
                return False
        else:
            return True
    else:
        return False

# fast

def is_prime_fast(number):
    if number > 1:
        for x in range(2, int(math.sqrt(number))):
            if number % x == 0:
                return False
        else:
            return True
    else:
        return False

# print(is_prime_fast(10))
for i in range(2, 100000000):
    if is_prime_fast(i):
        print(i)
