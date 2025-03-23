def go_bender(n, m, matrix):
    result = 0
    try:
        result = matrix[n][m]
    except IndexError:
        return result
    return result + go_bender(n + 1, m, matrix) if go_bender(n + 1, m, matrix) > go_bender(n, m + 1, matrix) else result + go_bender(n, m + 1, matrix)


n, m = map(int, input().split())
matrix = [list(map(int, input().split())) for _ in range(n)]

print(go_bender(0, 0, matrix))
