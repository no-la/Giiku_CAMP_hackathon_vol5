from config import settings
from utils import file_utils
import random

class NumerOnApp:
    def __init__(self, origin: str) -> None:
        self.n = 0
        self.origin = origin

    def increment(self):
        self.n += 1
        
    def judge(self, target: str) -> tuple[int, int]:
        eat = 0
        bite = 0

        # Eatをカウント
        for i in range(len(target)):
            if target[i] == self.origin[i]:
                eat += 1

        # 各数字の出現回数をカウント
        targets_counts = {str(d): target.count(str(d)) for d in range(10)}
        origin_counts = {str(d): self.origin.count(str(d)) for d in range(10)}

        # Biteをカウント
        for digit in targets_counts:
            if digit in origin_counts:
                bite += min(targets_counts[digit], origin_counts[digit])

        return eat, bite
    
def random_number(self, digit: int) -> str:
    # 10^digit - 1の範囲で乱数を生成し、ゼロパディング
    self.random_number = random.randint(0, 10**digit - 1)
    # ゼロパディングを行って指定された桁数の文字列を生成
    return f"{self.random_number:0{digit}d}"
    
