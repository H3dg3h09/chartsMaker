import random
from datetime import datetime

import pandas as pd
from faker import Faker

from ChartsMaker.main import ChartMaker, ChartReq
from ChartsMaker.schema import DataQuerySchema

fake = Faker(locale="zh_CN")
cm = ChartMaker()
df = pd.DataFrame(
    [[random.randint(0, 100) for _ in range(10)], [fake.date_between_dates(datetime(2023, 1, 1), datetime(2023, 10, 1)) for _ in range(10)]],
    index=["value", "date"],
).T

dq = DataQuerySchema(
    start_at=datetime(2023, 5, 1),
    end_at=datetime(2023, 8, 1),
)
req = ChartReq(type="line", x="date", y="value", y_name="数据名称", dimension="M", date=dq)
res = cm.make_charts(data=df, reqs=[req])
print([i.dict() for i in res])
