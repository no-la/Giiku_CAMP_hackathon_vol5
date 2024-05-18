from config import settings
from utils import file_utils


EMPTY = "."
COLORS = ["W", "B"]
class Gomoku:
    def __init__(self, n: int) -> None:
        self.n = n
        self.board = [[EMPTY]*n for _ in range(n)]
        self.count = 0
        self.win_num = 5
    
    def put_piece(self, x: int, y: int):
        """駒を(x, y)におく"""
        if not (0<=x<self.n and 0<=y<self.n):
            raise IndexError(f"碁盤の外に置こうとしています。 (x, y)={x, y}")
        if self.board[x][y]!=EMPTY:
            raise ValueError(f"すでに置かれています {self.board[x][y]} at ({x, y})")
        
        self.board[x][y] = COLORS[self.count^1]
    
    def judge(self, x: int, y: int):
        """(x, y)に置いた時の勝敗の判定"""
        for dx, dy in [[1, -1],[-1, 1],[-1, -1],[1, 1]]:
            for i in range(-self.win_num+1, self.win_num):
                nx, ny = x+dx*i, y+dy*i
                if self.board[nx][ny]:
                    ...
