import json
import random
from datetime import datetime

import pandas as pd
from faker import Faker

from ChartsMaker.main import ChartMaker, ChartReq, PieChart

fake = Faker(locale="zh_CN")

df = pd.DataFrame(
    [
        [random.randint(0, 100) for _ in range(10)],
        [random.random() * 10 for _ in range(10)],
        [fake.date_between_dates(datetime(2023, 1, 1), datetime(2023, 10, 1)) for _ in range(10)],
    ],
    index=["value", "float_value", "date"],
).T

json_str = """{"barMaxWidth": 15, "type": "line", "stack": null, "emphasis": {"focus": "series"}, "showSymbol": false}"""
cm = ChartMaker()
t_bar = ChartReq(type="bar", x="date", y="value", y_name="数据名称", custom_filed=json.loads(json_str))
res = cm.make_charts(data=df, reqs=t_bar)
print(res.dict())
t_line = ChartReq(type="line", x="date", y="value", y_name="数据名称")
res = cm.make_charts(data=df, reqs=t_line)
print(res.dict())

t_pie = PieChart(column_mapping={"数据名称": "value", "float": "float_value"}, y="date")
res = cm.make_charts(data=df, reqs=t_pie)
print(res.dict())

t_time = ChartReq(type="time", x="date", y="value", y_name="数据名称")
res = cm.make_charts(data=df, reqs=t_time)
print(res.dict())
