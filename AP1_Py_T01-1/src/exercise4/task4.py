import math

try:
    num = int(input())
except ValueError:
    print("Natural number was expected")
    exit()

if num < 0:
    print("Natural number was expected")
    exit()

m = 1
for n in range(num):
    for k in range(m):
        print(math.comb(n, k), end=" ")
    m += 1
    print()
