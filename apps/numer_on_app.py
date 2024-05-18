from config import settings
from utils import file_utils
import random
from enum import Enum
class NumerOnApp:
    def __init__(self, origin: str) -> None:
        # Invariant
        if not origin.isdigit():
            raise ValueError("The origin must be a numeric string.")
        
        self.judge_count = 0
        self.origin = origin

    def judge(self, target: str) -> tuple[int, int]:
        eat = 0
        bite = 0
        
        # Precondition
        if(len(target) != len(self.origin)):
            raise ValueError("The length of the target is different from the length of the origin.")
        if not target.isdigit():
            raise ValueError("The target must be a numeric string.")

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
        
        # judge_countをインクリメント
        self.judge_count += 1

        return eat, bite

class NumerOnAppState(Enum):
    INIT = 0
    PLAYING = 1
    FINISHED = 2
    
    
def random_number(digit: int) -> str:
    # 10^digit - 1の範囲で乱数を生成し、ゼロパディング
    random_number = random.randint(0, 10**digit - 1)
    # ゼロパディングを行って指定された桁数の文字列を生成
    return f"{random_number:0{digit}d}"
    
