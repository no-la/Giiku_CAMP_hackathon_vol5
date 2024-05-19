from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import settings
from utils import file_utils
from tests import conftest
from apps import numer_on_app
from apps import gomoku_app

from apps import just_time_app
from apps import help_app
from apps import stats_app