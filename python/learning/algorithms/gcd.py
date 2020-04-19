# Program computing the GCD using Euclid's algorithm

def gcd(a, b):
    divisor = a if a <= b else b
    dividend = a if a >= b else b
    while(divisor != 0):
        remainder = dividend % divisor
        dividend = divisor
        divisor = remainder
    return dividend

def find_gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

# def find_gcd_list

x=21
y=22
# print(gcd(x, y))
print(find_gcd(x,y))
