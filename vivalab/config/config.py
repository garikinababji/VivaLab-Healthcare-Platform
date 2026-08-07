import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "settings.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    CONFIG = json.load(file)

PROJECT_ID = CONFIG["project_id"]
ENVIRONMENT = CONFIG["environment"]

BUCKETS = CONFIG["buckets"]
DATASETS = CONFIG["datasets"]
TABLES = CONFIG["tables"]

REJECT_THRESHOLD = CONFIG["reject_threshold"]
LOG_LEVEL = CONFIG["log_level"]