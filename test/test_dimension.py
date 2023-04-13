import random
from datetime import datetime

import pandas as pd
from faker import Faker

from ChartsMaker.main import ChartMaker, ChartReq

fake = Faker(locale="zh_CN")
cm = ChartMaker()
df = pd.DataFrame(
    [[random.randint(0, 100) for _ in range(10)], [fake.date_between_dates(datetime(2023, 1, 1), datetime(2023, 10, 1)) for _ in range(10)]],
    index=["value", "date"],
).T

req_w = ChartReq(type="bar", x="date", y="value", y_name="数据名称", dimension="W")
req_m = ChartReq(type="bar", x="date", y="value", y_name="数据名称", dimension="M")
req_q = ChartReq(type="bar", x="date", y="value", y_name="数据名称", dimension="Q")
req_y = ChartReq(type="bar", x="date", y="value", y_name="数据名称", dimension="Y")

res = cm.make_charts(data=df, reqs=[req_w, req_m, req_q, req_y])
print([i.dict() for i in res])
