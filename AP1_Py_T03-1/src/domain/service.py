from src.domain.model import DomainModel, NOUGHT, CROSS

from typing import List, Tuple


class DomainService:
    def __init__(self):
        self.model = DomainModel()

    def validate(self, model: DomainModel) -> bool:
        count = 0 
        for i in range(3):
            for j in range(3):
                if self.model.board[i][j] != model.board[i][j]:
                    if self.model.board[i][j] is not None:
                        return False
                    if model.board[i][j] != CROSS:
                        return False
                    count += 1
        return count == 1


    def computer_move(self):
        best_move = self.minimax(self.model.board, NOUGHT, True)
        i, j = best_move[1], best_move[2]
        self.model.board[i][j] = NOUGHT

    def minimax(self, board: List[List[str]], depth: int, is_maximizing: bool) -> Tuple[int, int, int]:
        winner = self.check_winner()
        if winner == NOUGHT:
            return 10 - depth, None, None 
        elif winner == CROSS:
            return depth - 10, None, None 
        elif all(cell is not None for row in board for cell in row):
            return 0, None, None

        if is_maximizing:
            best_score = -float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = NOUGHT
                        score = self.minimax(board, depth + 1, False)[0]
                        board[i][j] = None  
                        if score > best_score:
                            best_score = score
                            best_move = (score, i, j)
            return best_move
        else:
            best_score = float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] is None:
                        board[i][j] = CROSS 
                        score = self.minimax(board, depth + 1, True)[0]
                        board[i][j] = None  
                        if score < best_score:
                            best_score = score
                            best_move = (score, i, j)
            return best_move

    def game_over(self):
        return self.model.game_over()

    def check_winner(self):
        return self.model.get_winner()


