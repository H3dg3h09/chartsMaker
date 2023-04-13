# type: ignore
from typing import Dict, List, Optional, TypeVar, Union

import pandas as pd

from .constants import StatisticsCycle
from .schema import BarMeta, ChartMeta, ChartReq, ChartResponse, LineMeta, PieChart, PieMeta, TimeMeta

T = TypeVar("T", bound=ChartReq)
K = TypeVar("K", bound=ChartMeta)


class ChartMaker:
    schema_mapping = {
        "line": LineMeta,
        "bar": BarMeta,
        "pie": PieMeta,
        "time": TimeMeta,
    }

    def __init__(self, date_column_name: Optional[str] = "date") -> None:
        self.date_column_name = date_column_name
        self.func_mapping = {
            "bar": self._bar,
            "line": self._line,
            "pie": self._pie,
            "time": self._time,
        }

    def make_charts(self, *, data: pd.DataFrame, reqs: Union[List[ChartReq], ChartReq]) -> List[Dict[str, ChartResponse]]:
        """
        生成图表
        :param data: 数据
        :param reqs: 需要的图标
        :return:
        """
        if not isinstance(reqs, list):
            return self._make_chart(data=data, params=reqs)
        return [self._make_chart(data=data, params=req) for req in reqs]

    def _make_chart(
        self,
        *,
        data: pd.DataFrame,
        params: T,
    ) -> ChartResponse:
        if not params.x:
            if not self.date_column_name:
                raise ValueError(f"x坐标轴字段名缺失, 请设置{self.__class__.__name__}.date_column_name 或 ChartReq.x")
            params.x = self.date_column_name

        if params.y not in data.columns or params.x not in data.columns:
            raise KeyError(f"所选列不在数据中, x: {params.x}或y: {params.y}")

        if isinstance(params, PieChart):
            if any([k not in data.columns for k in params.column_mapping.values()]):
                raise KeyError(f"所选列不在数据中, keys: {params.column_mapping.values()}")

        # 根据时间聚合
        data = self.re_agg_by_date(data, params)  # type: ignore
        func = self.func_mapping[params.type_]
        # 根据图表type来生成图表
        return func(data=data, params=params)

    @classmethod
    def _common(
        cls,
        data: pd.DataFrame,
        params: PieChart,
        chart_schema: T,
    ) -> ChartResponse[K]:
        return ChartResponse(
            x_data=data[params.x].to_list(),
            series=chart_schema(
                name=params.y_name,
                data=data[params.y].to_list(),
                custom=params.custom_filed,
            ),
        )

    @classmethod
    def _pie(
        cls,
        data: pd.DataFrame,
        params: PieChart,
    ) -> ChartResponse[PieMeta]:
        series = []
        for k, v in params.column_mapping.items():
            series.append(PieMeta(name=k, value=data[v][0]))
        return ChartResponse(series=series)

    @classmethod
    def _bar(
        cls,
        data: pd.DataFrame,
        params: T,
    ) -> ChartResponse[BarMeta]:
        return cls._common(data=data, params=params, chart_schema=BarMeta)

    @classmethod
    def _line(
        cls,
        data: pd.DataFrame,
        params: T,
    ) -> ChartResponse[LineMeta]:
        return cls._common(data=data, params=params, chart_schema=LineMeta)

    @classmethod
    def _time(
        cls,
        data: pd.DataFrame,
        params: PieChart,
    ) -> ChartResponse[TimeMeta]:
        data = data[[params.x, params.y]].T
        return ChartResponse(series=TimeMeta(data=list(data.to_dict("list").values()), name=params.y_name))

    @classmethod
    def re_agg_by_date(
        cls,
        data: pd.DataFrame,
        params: T,
    ) -> pd.DataFrame:
        try:
            data[params.x] = pd.to_datetime(data[params.x])
        except Exception:
            raise ValueError("x must be datetime or datetime's string.")

        if params.date:
            data = params.date.split_df(data)

        if not params.dimension or params.dimension == StatisticsCycle.DAILY:
            data[params.x] = data[params.x].dt.strftime(StatisticsCycle.format(StatisticsCycle.DAILY.value))
            return data

        dimension = params.dimension
        # 根据维度来转换时间'
        aggr = data.set_index(params.x).resample(dimension.value).sum()
        aggr.reset_index(inplace=True)

        aggr[params.x] = aggr[params.x].dt.strftime(StatisticsCycle.format(dimension.value))
        return aggr
