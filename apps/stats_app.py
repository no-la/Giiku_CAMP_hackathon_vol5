import datetime

from config import settings
from utils import file_utils


STATS_JSON_PATH = file_utils.join_path(settings.RESOURCE_DIR_PATH, "stats.json")


def save_stats(game_name: str, participant_ids: list, winner_id: int):
    """statsを保存する
    
    Parameters
    ----------
    game_name : str
        ゲームの種類
    participant_ids : list of int
        参加者のdiscordアカウントのid
    winner_id : int
        勝者のdiscordアカウントのid
    """
    d = load_stats()
    d["stats"].append({
        "time": datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), 
        "name": game_name,
        "participant_ids": participant_ids,
        "winner_id": winner_id
        })
    file_utils.write_jsonfile(STATS_JSON_PATH, d)
    
def load_stats() -> dict:
    return file_utils.get_dict_from_jsonfile(STATS_JSON_PATH)

