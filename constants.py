from enum import Enum


class StatisticsCycle(Enum):
    """统计维度"""

    DAILY = "D"  # 日
    WEEKLY = "W"  # 周
    MONTHLY = "M"  # 月
    QUARTER = "Q"  # 季
    ANNUAL = "Y"  # 年

    @staticmethod
    def format(s):
        mapping = {
            "D": "%Y-%m-%d",  # 日
            "W": "%Y-%W",  # 周
            "M": "%Y-%m",  # 月
            "Q": "%Y-%Q",  # 季
            "Y": "%Y",  # 年
        }
        try:
            return mapping[s]
        except KeyError:
            raise KeyError("聚合暂只支持D(日), W(周), M(月), Q(季), Y(年)")


class StatisticsFormatString(Enum):
    """统计维度"""

    DAILY = "%Y-%m-%d"  # 日
    WEEKLY = "%Y-%W"  # 周
    MONTHLY = "%Y-%m"  # 月
    QUARTER = "%Y-%Q"  # 季
    ANNUAL = "%Y"  # 年
