from datetime import datetime
from typing import NamedTuple


class Schedule(NamedTuple):
    datetime: datetime
    event: str
    type: str


schedule_data = [
    Schedule(datetime(2025, 6, 27, 18, 0), '【予選】部屋建て期限1時間前', '【予選】'),
    Schedule(datetime(2025, 6, 27, 19, 0), '【予選】入室期限1時間前', '【予選】'),
    Schedule(datetime(2025, 6, 27, 20, 0), '【予選】結果提出期限1時間前', '【予選】'),
    Schedule(datetime(2025, 6, 28, 18, 0), '【勝者側-準々決】【敗者側-予選】部屋建て期限1時間前', '【勝者側-準々決】【敗者側-予選】'),
    Schedule(datetime(2025, 6, 28, 19, 0), '【勝者側-準々決】【敗者側-予選】入室期限1時間前', '【勝者側-準々決】【敗者側-予選】'),
    Schedule(datetime(2025, 6, 28, 20, 0), '【勝者側-準々決】【敗者側-予選】結果提出期限1時間前', '【勝者側-準々決】【敗者側-予選】'),
    Schedule(datetime(2025, 6, 29, 12, 0), '【勝者側-準決】【敗者側-準々決】部屋建て期限1時間前', '【勝者側-準決】【敗者側-準々決】'),
    Schedule(datetime(2025, 6, 29, 13, 0), '【勝者側-準決】【敗者側-準々決】入室期限1時間前', '【勝者側-準決】【敗者側-準々決】'),
    Schedule(datetime(2025, 6, 29, 14, 0), '【勝者側-準決】【敗者側-準々決】結果提出期限1時間前', '【勝者側-準決】【敗者側-準々決】'),
    Schedule(datetime(2025, 6, 29, 19, 0), '【敗者側-準決】部屋建て期限1時間前', '【敗者側-準決】'),
    Schedule(datetime(2025, 6, 29, 20, 0), '【敗者側-準決】入室期限1時間前', '【敗者側-準決】'),
    Schedule(datetime(2025, 6, 29, 21, 0), '【敗者側-準決】結果提出期限1時間前', '【敗者側-準決】'),
]
