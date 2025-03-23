def count_neighbours(data, x, y):
    counter = 0
    try:
        if data[x][y] == 1:
            counter += 1
            data[x][y] = 0
            counter += count_neighbours(data, x, y + 1)
            counter += count_neighbours(data, x + 1, y - 1)
            counter += count_neighbours(data, x + 1, y)
            counter += count_neighbours(data, x + 1, y + 1)
        return counter
    except IndexError:
        return 0

def is_square(data, x, y):
    side_size = 0
    try:
        while data[x + side_size][y] == 1:
            side_size += 1
    except IndexError:
        pass
    count = count_neighbours(data, x, y)
    return True if side_size ** 2 == count and count != 0 else False

def figure_counter(data):
    square = 0
    circle = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 1:
                if is_square(data, i, j):
                    square += 1
                else:
                    circle += 1

    return square, circle


def main():
    with open('input.txt') as file:
        lines = file.readlines()

    data = [list(map(int, line.split())) for line in lines]
    print(figure_counter(data))


if __name__ == '__main__':
    main()