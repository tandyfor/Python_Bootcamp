a = list(map(float, input().split()))
b = list(map(float, input().split()))
result = sum(list(map(lambda x, y: x * y, a, b)))
print(result)