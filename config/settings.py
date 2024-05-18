import json
from pathlib import Path

from utils import file_utils


with open("secret.json", "r", encoding="utf-8") as f:
    TOKEN = json.load(f)["discord"]["token"]

GUILD_ID = 948364589115002880

ENCODING = "utf-8"

ROOT_DIR_PATH = str(Path(__file__).parent.parent)
CONFIG_DIR_PATH = file_utils.join_path(ROOT_DIR_PATH, "config")
APP_DIR_PATH = file_utils.join_path(ROOT_DIR_PATH, "apps")
COG_DIR_PATH = file_utils.join_path(ROOT_DIR_PATH, "cogs")
TEST_DIR_PATH = file_utils.join_path(ROOT_DIR_PATH, "tests")
RESOURCE_DIR_PATH = file_utils.join_path(ROOT_DIR_PATH, "resources")

