from typing import TypeVar, Union
from adapter.base import AdapterBase
from sqlalchemy.orm import DeclarativeBase
from tortoise.models import Model
import pandas as pd


SQLAlchemyBaseModel = TypeVar("SQLAlchemyBaseModel", bound=DeclarativeBase)
TortoiseBaseModel = TypeVar("TortoiseBaseModel", bound=Model)
SQLDataSeries = Union[SQLAlchemyBaseModel, TortoiseBaseModel]


class MySQLAdapter(AdapterBase):
    def __init__(self, data: SQLDataSeries):
        super().__init__(data)

    def to_df(self):
        return pd.DataFrame(self.data)
