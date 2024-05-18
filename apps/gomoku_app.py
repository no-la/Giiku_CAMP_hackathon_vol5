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
        self.winner = None
    
    def get_turn(self):
        """0が先手番"""
        return self.count&1
    
    def put_piece(self, x: int, y: int):
        """駒を(x, y)におく"""
        if not (0<=x<self.n and 0<=y<self.n):
            raise IndexError(f"碁盤の外に置こうとしています。 (x, y)={x, y}")
        if self.board[x][y]!=EMPTY:
            raise ValueError(f"すでに置かれています {self.board[x][y]} at {x, y}")
        if self.winner is not None:
            raise ValueError("すでにゲームが終了しています")
        
        self.board[x][y] = self.get_turn()
        
        if self.judge():
            self.fin(self.get_turn())
        else:
            self.count += 1
            if self.count == self.n**2:
                self.fin(-1)
    
    def judge(self):
        """ゲームの決着の判定"""
        for x in range(self.n):
            for y in range(self.n):
                for dx, dy in [[1, -1], [1, 1], [1, 0], [0, 1]]:
                    for i in range(1, self.win_num):
                        nx, ny = x+dx*i, y+dy*i
                        if not (0<=nx<self.n and 0<=ny<self.n):
                            break
                        if self.board[nx][ny] != self.get_turn():
                            break
                    else:
                        return True
        return False
    
    def fin(self, winner: int):
        self.winner = winner
    
    def __str__(self) -> str:
        rev = "".join(map(str, self.board[0]))
        for l in self.board[1:]:
            rev += "\n"+"".join(map(str, l))
        return rev
