import random
from datetime import datetime

import pandas as pd
from faker import Faker

from ChartsMaker.main import ChartMaker, ChartReq, PieChart

fake = Faker(locale="zh_CN")

df = pd.DataFrame(
    [[random.randint(0, 100) for _ in range(10)], [fake.date_between_dates(datetime(2023, 1, 1), datetime(2023, 10, 1)) for _ in range(10)]],
    index=["value", "date"],
).T


cm = ChartMaker()
t_bar = ChartReq(type="bar", x="date", y="value", y_name="数据名称")
res = cm.make_charts(data=df, reqs=[t_bar])
print([i.dict() for i in res])

t_line = ChartReq(type="line", x="date", y="value", y_name="数据名称")
res = cm.make_charts(data=df, reqs=[t_bar])
print([i.dict() for i in res])

t_pie = PieChart(column_mapping={"数据名称": "value"}, y="date")
res = cm.make_charts(data=df, reqs=[t_pie])
print([i.dict() for i in res])

t_time = ChartReq(type="time", x="date", y="value", y_name="数据名称")
res = cm.make_charts(data=df, reqs=[t_time])
print([i.dict() for i in res])
