from PIL import Image, ImageDraw

from config import settings
from utils import file_utils


EMPTY = "."
class Gomoku:
    def __init__(self, n: int) -> None:
        self.n = n
        self.board = [[EMPTY]*n for _ in range(n)]
        self.count = 0
        self.win_num = 3
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
                    for i in range(self.win_num):
                        nx, ny = x+dx*i, y+dy*i
                        if not (0<=nx<self.n and 0<=ny<self.n):
                            break
                        if self.board[nx][ny] != self.get_turn():
                            break
                    else:
                        print("fin gomoku", (x, y), "to", (nx, ny))
                        return True
        return False
    
    def fin(self, winner: int):
        self.winner = winner
    
    def __str__(self) -> str:
        rev = "".join(map(str, self.board[0]))
        for l in self.board[1:]:
            rev += "\n"+"".join(map(str, l))
        return rev
        
    def get_formatted_board(self):
        rev = "".join(map(lambda x: self.get_fomatted_element(x), self.board[0]))
        for l in self.board[1:]:
            rev += "\n" + "".join(map(lambda x: self.get_fomatted_element(x), l))
        return rev
    
    def get_fomatted_element(self, tar: int|str):
        COLORS = ["⚪", "⚫"]
        return COLORS[tar] if isinstance(tar, int) else "🟦"

    def make_board_img(self):
        x = 30
        img = Image.new("RGB", (self.n*x, self.n*x), (256, 256, 256))
        img.save()