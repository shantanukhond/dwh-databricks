"""File-drop generator for the Auto Loader lesson.

Writes small JSON files (a few orders each) into a UC volume at intervals,
so `cloudFiles` always has fresh input — without any external storage.

Run inside the Auto Loader notebook AFTER starting your stream in another cell:

    from generate_files import run
    run("/Volumes/sandbox/ingest/landing/orders", minutes=10, per_minute=2)
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
import uuid

CITIES = ["Bengaluru", "Mexico City", "Mumbai", "Berlin", "Dubai",
          "Austin", "Singapore", "Milan", "Tokyo", "Arlington"]


def make_batch(n: int = 5) -> list[dict]:
    """A handful of order-ish events."""
    return [
        {
            "event_id": str(uuid.uuid4()),
            "customer_id": random.randint(1, 20),
            "amount": round(random.uniform(5, 500), 2),
            "city": random.choice(CITIES),
            "event_ts": int(time.time() * 1000),
        }
        for _ in range(n)
    ]


def run(volume_path: str, minutes: float = 10.0, per_minute: float = 2.0,
        files_per_drop: int = 1) -> None:
    interval = 60.0 / per_minute
    deadline = time.monotonic() + minutes * 60.0
    os.makedirs(volume_path, exist_ok=True)
    n = 0

    print(f"Dropping {files_per_drop} file(s) into {volume_path} "
          f"every {interval:.0f}s for {minutes:.0f} min …")
    while time.monotonic() < deadline:
        for _ in range(files_per_drop):
            path = os.path.join(volume_path, f"orders-{int(time.time())}-{uuid.uuid4().hex[:6]}.json")
            with open(path, "w", encoding="utf-8") as f:
                for row in make_batch():
                    f.write(json.dumps(row) + "\n")   # JSON-lines: one record per line
            n += 1
        if n % 5 == 0:
            print(f"  …{n} files written")
        time.sleep(interval)

    print(f"Done — {n} files written.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("volume_path", help="e.g. /Volumes/sandbox/ingest/landing/orders")
    ap.add_argument("--minutes", type=float, default=10.0)
    ap.add_argument("--per-minute", type=float, default=2.0)
    args = ap.parse_args()
    run(args.volume_path, minutes=args.minutes, per_minute=args.per_minute)
