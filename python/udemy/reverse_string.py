def reverse_string(string):
    if type(string) != str:
        print("k")
    return string[::-1]

def reverse_string2(string):
    reversed = []
    i = len(string) - 1
    while i >= 0:
        reversed.append(string[i])
        i -= 1
    return ''.join(reversed)

def reverse_string3(string):
    return string.reverse()

print(reverse_string3("hello"))
