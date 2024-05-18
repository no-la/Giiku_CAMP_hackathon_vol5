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

        # Eatの分を引く
        bite -= eat
        
        # judge_countをインクリメント
        self.judge_count += 1

        return eat, bite

class NumerOnAppState(Enum):
    INIT = 0
    PLAYING = 1
    FINISHED = 2
class NumerOnAppManager:
    def __init__(self, digit: int) -> None:
        self.digit = digit
        self.state = NumerOnAppState.INIT
        self.app = None

    def start(self) -> str:
        self.state = NumerOnAppState.PLAYING
        self.app = NumerOnApp(random_number(self.digit))
        return self.app.origin
    
    def update(self, message: str) -> None:
        if self.state == NumerOnAppState.INIT:
            raise ValueError("The game has not started yet.")
        elif self.state == NumerOnAppState.FINISHED:
            raise ValueError("The game has already finished.")
        else :
             self.judge(message)

    def judge(self, target: str) -> tuple[int, int]:
        if self.state != NumerOnAppState.PLAYING:
            raise ValueError("The game is not in progress.")
        return self.app.judge(target)

    def finish(self) -> None:
        self.state = NumerOnAppState.FINISHED

    def is_finished(self) -> bool:
        return self.state == NumerOnAppState.FINISHED

    def is_playing(self) -> bool:
        return self.state == NumerOnAppState.PLAYING

    def is_init(self) -> bool:
        return self.state == NumerOnAppState.INIT

    def get_judge_count(self) -> int:
        return self.app.judge_count

    def get_origin(self) -> str:
        return self.app.origin

    def get_digit(self) -> int:
        return self.digit

    def get_state(self) -> NumerOnAppState:
        return self.state

    def reset(self) -> None:
        self.state = NumerOnAppState.INIT
        self.app = None

    def __str__(self) -> str:
        return f"NumerOnAppManager(digit={self.digit}, state={self.state}, app={self.app})"

    def __repr__(self) -> str:
        return self.__str__()


    
    
def random_number(digit: int) -> str:
    # 10^digit - 1の範囲で乱数を生成し、ゼロパディング
    random_number = random.randint(0, 10**digit - 1)
    # ゼロパディングを行って指定された桁数の文字列を生成
    return f"{random_number:0{digit}d}"
    
