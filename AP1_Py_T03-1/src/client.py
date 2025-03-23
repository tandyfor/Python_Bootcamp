import requests
import json

URL = 'http://127.0.0.1:5000/game/'
CROSS = 1

def pos_2_ij(pos):
    pos -= 1
    return pos // 3, pos % 3

def start_game():
    responce = requests.get(URL, allow_redirects=True)
    if responce.status_code != 200:
        print(responce.status_code)
        exit()

    print(f"status: {responce.status_code}")
    print(f"url: {responce.url}")
    print(f"json: {responce.text}")
    
    return responce.url, responce.text

def move(url, data):
    i, j = pos_2_ij(int(input("Input position: ")))

    data = json.loads(data)
    board = data.get('board')

    print(board)
    board[i][j] = CROSS
    data['board'] = board

    print(data)
    
    responce = requests.post(url, json=data)

    if responce.status_code != 200:
        print(responce.status_code)
        exit()

    print(f"status: {responce.status_code}")
    print(f"url: {responce.url}")
    print(f"json: {responce.text}")

    return responce.text

if __name__ == '__main__':
    url, data = start_game()
    while True:
        data = move(url, data)

