import requests
import pandas as pd
import time
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
HEADERS = {}  # add {"X-App-Token": "TOKEN"}
START, END = "2025-01-01T00:00:00", "2025-01-31T23:59:59"
PAGE, MAX_ROWS = 50000, 200000

rows, offset = [], 0
while offset < MAX_ROWS:
    params = {
        "$where": f"created_date between '{START}' and '{END}'",
        "$limit": PAGE,
        "$offset": offset,
        "$order": "created_date, unique_key",
    }
    r = requests.get(URL, params=params, headers=HEADERS, timeout=120)
    r.raise_for_status()
    batch = r.json()
    if not batch:
        break
    rows.extend(batch)
    offset += PAGE
    print(f"Pulled {len(rows)} rows")
    time.sleep(1)

pd.DataFrame(rows).to_csv(RAW / "311_raw.csv", index=False)
print("Saved", len(rows), "rows")