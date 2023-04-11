from typing import TypeVar, Union
from adapter.base import AdapterBase
import pandas as pd

MongoDataSeries = TypeVar("MongoDataSeries")  # TODO: 兼容pymongo, motor查询结果


class MongoAdapter(AdapterBase):
    def __init__(self, data: MongoDataSeries):
        super().__init__(data)

    def to_df(self):
        return pd.DataFrame(self.data)
