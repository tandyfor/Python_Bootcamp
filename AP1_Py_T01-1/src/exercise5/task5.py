# print(f"{eval(input() + " * 2"):.3f}") # Pythonic!

string = input()

ALLOWED_SYMBOLS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.', '+']

number = 0
sign = 1
scale = 0

for symbol in string:
    if symbol not in ALLOWED_SYMBOLS:
        print(f"Invalid symbol: {symbol}")
        exit()
    number *= 10
    match symbol:
        case '0':
            pass
        case '1':
            number += 1
        case '2':
            number += 2
        case '3':
            number += 3
        case '4':
            number += 4
        case '5':
            number += 5
        case '6':
            number += 6
        case '7':
            number += 7
        case '8':
            number += 8
        case '9':
            number += 9
        case '-':
            sign *= -1
        case '.':
            scale = 0.1
            number /= 10
    scale *= 10

number *= sign
if scale!= 0:
    number /= scale

print(f"{number * 2:.3f}")
            
