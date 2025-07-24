import json
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = "last_scrape.json"

def parse_z_isoformat(s: str):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def load_last_scrape_time() -> datetime:
    if not Path(STATE_FILE).exists():
        return datetime.min.replace(tzinfo=timezone.utc)

    with open(STATE_FILE, "r") as f:
        ts = json.load(f).get("last_scrape_time")
        return parse_z_isoformat(ts)

def save_current_scrape_time(time: datetime):
    iso_str = time.isoformat()
    if iso_str.endswith("+00:00"):
        iso_str = iso_str.replace("+00:00", "Z")
    with open(STATE_FILE, "w") as f:
        json.dump({"last_scrape_time": iso_str}, f)