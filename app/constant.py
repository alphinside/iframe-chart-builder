from enum import Enum, EnumMeta
from pathlib import Path

CHARTS_ROUTE = "/chart/"
TABLES_ROUTE = "/table/"
STANDARD_CHARTS_CONFIG = Path("charts_config.json")
STANDARD_STYLE_CONFIG = Path("style_config.json")
STANDARD_DATA_FILENAME = Path("data.gzip")
DASH_MOUNT_ROUTE = "/app"
DASH_ROOT_ROUTE = DASH_MOUNT_ROUTE + "/"
MAX_NUMBER_FILTERS = 5

# CALLBACK TYPES
COLUMN_FILTER_CAT = "column-filter-categorical"
COLUMN_FILTER_NUM_MIN = "column-filter-numerical-min"
COLUMN_FILTER_NUM_MAX = "column-filter-numerical-max"
COLUMN_FILTER_SELECT_ALL = "column-filter-select-all"
SELECT_ALL_VALUE = "select-all"


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class ChartTypes(str, BaseEnum):
    bar = "bar"
    choropleth_map = "choropleth_map"
    bubble_map = "bubble_map"


class DataTypes(str, BaseEnum):
    numerical = "numerical"
    categorical = "categorical"


class ResourceType(str, BaseEnum):
    chart = "chart"
    table = "table"


class PlotlyColorGroup(str, BaseEnum):
    qualitative = "qualitative"
    sequential = "sequential"
    diverging = "diverging"
    cyclical = "cyclical"
