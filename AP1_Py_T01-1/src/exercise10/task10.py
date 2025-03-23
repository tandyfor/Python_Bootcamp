try:
    n, time = map(int, input().split())
    machines = [list(map(int, input().split())) for _ in range(n)]
except:
    print("Input error!")
    exit()
else:
    for i in machines:
        if len(i) != 3:
            print("Input error!")
            exit()


years = list(map(lambda x: x[0], machines))
years_to_remove = list(filter(lambda x: years.count(x) == 1, years))
machines = list(filter(lambda x: x[0] not in years_to_remove, machines))
machines.sort(key=lambda x: x[1])

coasts = []

for i in machines:
    for j in machines:
        if i == j:
            continue
        if i[2] + j[2] == time:
            coasts.append(i[1] + j[1])

print(min(coasts))
