import json

try:
    with open('input.txt') as f:
        data = json.load(f)
except:
    print("Input error!")
    exit()


for key in list(data.keys()):
    if not data.get("list0"): # Здесь немного не ясно под каким ключом должен сохраняться новый список. Я оставил как в примере.
        data["list0"] = data[key]
    else:
        data["list0"] = data["list0"] + data[key]
    del data[key]

data["list0"] = sorted(data.get("list0"), key= lambda x: x.get("year"))

new_data = json.dumps(data, indent=4)
print(new_data)
