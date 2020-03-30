# Program computing the GCD using Euclid's algorithm

def gcd(a, b):
    divisor = a if a <= b else b
    dividend = a if a >= b else b
    while(divisor != 0):
        remainder = dividend % divisor
        dividend = divisor
        divisor = remainder
    return dividend

print(gcd(40, 50))
