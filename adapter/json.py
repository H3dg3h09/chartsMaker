from typing import TypeVar, List, Dict, Any, Optional
from adapter.base import AdapterBase
import pandas as pd

JsonDataSeries = TypeVar("JsonDataSeries", List[Any], Dict["str", List[Any]])


class JsonAdapter(AdapterBase):
    """适配Json格式数据

    Args:
        AdapterBase (_type_): 仅支持list和dict类型
    """

    def __init__(self, data: JsonDataSeries):
        super().__init__(data)

    def to_df(self, columns: Optional[List[str]] = None) -> pd.DataFrame:
        return pd.DataFrame(self.data, columns=columns)
