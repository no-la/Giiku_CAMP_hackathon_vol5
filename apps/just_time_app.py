import datetime

from config import settings
from utils import file_utils

class JustTimeApp:
    def __init__(self) -> None:
        self.time = 0

    def start(self) -> None:
        self.time = 0

    def stop(self) -> None:
        pass

    def get_time(self) -> int:
        return self.time

    def set_time(self, time: int) -> None:
        self.time = time

    def add_time(self, time: int) -> None:
        self.time += time

    def sub_time(self, time: int) -> None:
        self.time -= time

    def reset_time(self) -> None:
        self.time = 0
        
class JustTimeAppManager:
    def __init__(self) -> None:
        self.app = JustTimeApp()
        self.start_time = None

    def start(self, start_time: datetime) -> None:
        self.start_time = start_time
    
    def judge(self, time: datetime) -> float:
        diff = time - self.start_time
        
        return diff.seconds + diff.microseconds / 1_000_000

    def stop(self) -> None:
        self.app.stop()