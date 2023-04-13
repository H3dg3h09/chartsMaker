from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import pandas as pd
from pydantic import BaseModel, Extra, Field, validator
from pydantic.generics import GenericModel

from .constants import StatisticsCycle

T = TypeVar("T")


class DataQuerySchema(BaseModel):
    """start 开, end 闭"""

    start_at: datetime = Field(description="开始时间")
    end_at: datetime = Field(description="结束时间")

    def split_df(self, data: pd.DataFrame):
        return data[(data["date"] >= self.start_at) & (data["date"] < self.end_at)]


class ChartBase(BaseModel, extra=Extra.allow):
    type_: str = Field(description="图标类型", alias="type")
    y: str = Field(description="y轴_数据列column_name")
    x: Optional[str] = Field(None, description="X轴_日期列column_name")
    y_name: Optional[str] = Field(None, description="y轴数据列的名称")

    custom_filed: Optional[Dict] = Field(None, description="自定义字段, like style")

    date: Optional[DataQuerySchema] = Field(None, description="时间筛选")
    dimension: Optional[StatisticsCycle] = Field(None, description="统计维度")

    @validator("y_name")
    def name_validator(cls, v, values):
        return v or values["column"]


class PieChart(ChartBase, BaseModel):
    type_: str = Field("pie", description="类型", alias="type")
    column_mapping: Dict[str, str] = Field(description="数据列, k=显示name, v=数据列名")


class ChartResponse(GenericModel, Generic[T]):
    x_data: Optional[List] = Field(None, description="x轴数据-类目轴")  # type_: ignore
    series: T = Field(default=None, description="数据")


class ChartMeta(BaseModel, extra=Extra.allow):
    custom: Optional[Dict] = Field(None, description="自定义字段")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        # 合并custom字段
        if getattr(self, "custom", None):
            for k, v in self.custom.items():  # type_: ignore
                setattr(self, k, v)
        self.custom = None

    def dict(self, *args, **kargs):
        kargs["exclude_none"] = True
        return super().dict(*args, **kargs)


class PieMeta(ChartMeta, BaseModel):
    type_: str = Field("pie", description="类型", alias="type")
    name: str = Field(..., description="名称")
    value: Optional[Union[float, int]] = Field(None, description="值")

    # def dict(self, *args, **kargs):
    #     d = super().dict(*args, **kargs)
    #     try:
    #         # 去掉base
    #         d.pop("data")
    #     except Exception:
    #         pass
    #     return d


class TimeMeta(ChartMeta, BaseModel):
    type_: str = Field("time", description="类型", alias="type")
    name: str = Field(..., description="名称")
    data: List[List] = Field(..., description="数据:[2022-11-01, 0]")


class BarMeta(ChartMeta, BaseModel):
    type_: str = Field("bar", description="类型", alias="type")
    name: str = Field(..., description="名称")
    data: List[Union[float, None]] = Field(None, description="数据")


class LineMeta(ChartMeta, BaseModel):
    type_: Optional[str] = Field("line", description="类型")
    data: List[Union[float, None]] = Field(..., description="数据")


def ChartReq(type: str, **kargs):
    charts_type = ["bar", "line", "pie", "time"]
    if type not in charts_type:
        raise TypeError(f"暂不支持图标类型{type}, 目前只支持: {charts_type}")

    if type == "pie":
        if not kargs.get("column_mapping"):
            raise ValueError("饼图pie必须设置column_mapping")
        return PieChart(column_mapping=kargs["column_mapping"])
    else:
        return ChartBase(type=type, **kargs)
