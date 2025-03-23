from uuid import uuid4

NOUGHT = 0
CROSS = 1

class DomainModel:
    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.uuid = uuid4()

    def __pos_2_ij(self, pos):
        if not (1 <= pos <= 9):
            raise ValueError("Position must be between 1 and 9.")
        pos -= 1
        return pos // 3, pos % 3

    def move(self, pos, player):
        i, j = self.__pos_2_ij(pos)
        
        if self.board[i][j] is not None:
            raise ValueError(f"Cell {pos} is already occupied.")
        
        self.board[i][j] = player

    def game_over(self):
        winner = self.check_winner()
        if winner == NOUGHT or winner == CROSS:
            return True

        if all(cell is not None for row in self.board for cell in row):
            return True

        return False

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] is not None:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                return self.board[0][i]
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        return None

    def get_winner(self):
        return self.check_winner()

if __name__ == '__main__':
    gb = DomainModel()
    print(gb.board)
    gb.move(5, NOUGHT)
    print(gb.board)
    gb.move(1, CROSS)
    print(gb.board)
    gb.move(9, CROSS)
    print(gb.board)
    print(gb.game_over())
    for i in range(1, 10):
        gb.move(i, CROSS)
    print(gb.board)
    print(gb.game_over())
    print(gb.uuid)