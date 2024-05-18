import datetime
from collections import defaultdict
from enum import Enum

from config import settings
from utils import file_utils

class JustTimeAppState(Enum):
    INIT = 0
    REGISTERING = 1
    PLAYING = 2
    FINISHED = 3
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
        self.state = JustTimeAppState.INIT
        self.start_time = None
        self.participant_ids = set() 
        self.participant_times = defaultdict(None)
    def add_participant(self, participant_id: int) -> None:
        self.participant_ids.add(participant_id)
        print(f"Added participant: {participant_id}")
    
    def register(self) -> None:
        self.state = JustTimeAppState.REGISTERING
    
    def start(self, start_time: datetime) -> None:
        self.start_time = start_time
        self.state = JustTimeAppState.PLAYING
    
    def record_time(self, participant_id: int, time: datetime) -> None:
        # Precondition
        if participant_id not in self.participant_ids:
            raise ValueError("The participant is not registered.")
        
        diff = time - self.start_time
        self.participant_times[participant_id] = (diff.seconds + diff.microseconds / 1_000_000)
        
    def is_finished(self) -> bool:
        return len(self.participant_times) == len(self.participant_ids)

    def get_diff(self) -> list[tuple[str, float]]:
        return [(str(participant_id), time) for participant_id, time in self.participant_times.items()]