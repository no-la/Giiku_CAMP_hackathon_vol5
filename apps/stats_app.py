import datetime

from config import settings
from utils import file_utils


STATS_JSON_PATH = file_utils.join_path(settings.RESOURCE_DIR_PATH, "stats.json")


def save_stats(game_name: str, participants: list, winner_id: int, time: datetime.datetime):
    d = load_stats()
    d["stats"].append(time.strftime('%Y/%m/%d %H:%M:%S'), game_name, participants, winner_id)
    file_utils.write_jsonfile(STATS_JSON_PATH, d)
    
def load_stats() -> dict:
    return file_utils.get_dict_from_jsonfile(STATS_JSON_PATH)

