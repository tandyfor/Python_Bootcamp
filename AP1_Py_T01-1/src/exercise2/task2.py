# Вариант где "не используются строки".

# inp_str = input()
# number = int(inp_str)

# if number < 0: 
#     print(False)
# else:
#     inp_list = list(inp_str)
#     rev = inp_list.copy()
#     rev.reverse()
#     if inp_list == rev:
#         print(True)
#     else:
#         print(False)

x = input()

if not x.find('-'):
    print(False)
    exit()

for i in range(round(len(x) / 2)):
    if x[i] != x[len(x)- i - 1]:
        print(False)
        exit()
else:
    print(True)