from datetime import datetime
from typing import NamedTuple

# datetime(2024, 9, 10, 8, 0): ("event", "type"),  # 2024/9/10 8:00
# ["予選", "勝者側-準々決", "勝者側-準決", "敗者側-予選", "敗者側-準々決", "敗者側-準決"]
# [部屋建て期限、入室期限、結果提出期限],[3時間前,1時間前,30分前]


class Schedule(NamedTuple):
    datetime: datetime
    event: str
    type: str


schedule_data = [
    Schedule(datetime(2025, 1, 30, 18, 0), "予選部屋建て期限1時間前", "予選"),
    Schedule(datetime(2025, 1, 30, 19, 0), "予選入室期限1時間前", "予選"),
    Schedule(datetime(2025, 1, 30, 20, 0), "予選結果提出期限1時間前", "予選"),
    Schedule(
        datetime(2025, 1, 31, 18, 0),
        "勝者側-準々決部屋建て期限1時間前",
        "勝者側-準々決",
    ),
    Schedule(
        datetime(2025, 1, 31, 19, 0), "勝者側-準々決入室期限1時間前", "勝者側-準々決"
    ),
    Schedule(
        datetime(2025, 1, 31, 20, 0),
        "勝者側-準々決結果提出期限1時間前",
        "勝者側-準々決",
    ),
    Schedule(
        datetime(2025, 2, 1, 12, 0), "勝者側-準決部屋建て期限1時間前", "勝者側-準決"
    ),
    Schedule(datetime(2025, 2, 1, 13, 0), "勝者側-準決入室期限1時間前", "勝者側-準決"),
    Schedule(
        datetime(2025, 2, 1, 14, 0), "勝者側-準決結果提出期限1時間前", "勝者側-準決"
    ),
    Schedule(
        datetime(2025, 1, 31, 18, 0), "敗者側-予選部屋建て期限1時間前", "敗者側-予選"
    ),
    Schedule(datetime(2025, 1, 31, 19, 0), "敗者側-予選入室期限1時間前", "敗者側-予選"),
    Schedule(
        datetime(2025, 1, 31, 20, 0), "敗者側-予選結果提出期限1時間前", "敗者側-予選"
    ),
    Schedule(
        datetime(2025, 2, 1, 12, 0), "敗者側-準々決部屋建て期限1時間前", "敗者側-準々決"
    ),
    Schedule(
        datetime(2025, 2, 1, 13, 0), "敗者側-準々決入室期限1時間前", "敗者側-準々決"
    ),
    Schedule(
        datetime(2025, 2, 1, 14, 0), "敗者側-準々決結果提出期限1時間前", "敗者側-準々決"
    ),
    Schedule(
        datetime(2025, 2, 1, 19, 0), "敗者側-準決部屋建て期限1時間前", "敗者側-準決"
    ),
    Schedule(datetime(2025, 2, 1, 20, 0), "敗者側-準決入室期限1時間前", "敗者側-準決"),
    Schedule(
        datetime(2025, 2, 1, 21, 0), "敗者側-準決結果提出期限1時間前", "敗者側-準決"
    ),
]
