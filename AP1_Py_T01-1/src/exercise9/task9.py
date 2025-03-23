# Формулировка задачи плохо поставлна.
# Возможно требуется реализация алгоритма. Чеклист покажет...

n, x = input().split()
a = float(input())
coef = float(input())
const = float(input())

print(f"{a * int(n) * float(x) ** (int(n) - 1) + coef:.3f}")