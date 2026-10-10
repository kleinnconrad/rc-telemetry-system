"""Convert the firmware log into a CSV file for spreadsheets and analysis tools.

The firmware appends one JSON object per line (JSON Lines) to /log.csv on the
microSD card, despite the .csv extension. The timestamp `ts` counts
milliseconds since boot, so a drop in `ts` marks a new power cycle; each
power cycle gets its own session number.

Run:  python scripts/log_to_csv.py LOG.CSV [OUTPUT.csv]
      (default output: <input name>_converted.csv next to the input)
"""

import csv
import json
import sys
from pathlib import Path

FIELDS = ["session", "ts", "time_s", "rpm", "t_m", "t_e", "lat", "lng", "spd"]


def convert(src, dst):
    rows, session, last_ts, skipped = [], 1, None, 0
    with src.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                ts = int(record["ts"])
            except (ValueError, KeyError, TypeError):
                skipped += 1  # e.g. a line cut off by a power loss during the write
                continue
            if last_ts is not None and ts < last_ts:
                session += 1
            last_ts = ts
            row = {key: record.get(key) for key in FIELDS}
            row.update(session=session, ts=ts, time_s=round(ts / 1000, 3))
            rows.append(row)

    with dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows), session if rows else 0, skipped


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) == 3 else src.with_name(f"{src.stem}_converted.csv")
    count, sessions, skipped = convert(src, dst)
    print(f"Wrote {count} records from {sessions} session(s) to {dst} ({skipped} invalid lines skipped)")


if __name__ == "__main__":
    main()
