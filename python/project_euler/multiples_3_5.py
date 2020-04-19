
total = 0
n = 1000
for i in range(3, n):
    print(i)
    if i % 3 == 0 or i % 5 == 0:
        total += i
print(total)
