from enum import Enum, EnumMeta
from pathlib import Path

CHARTS_ROUTE = "/charts/"
TABLES_ROUTE = "/tables/"
STANDARD_CHARTS_CONFIG = Path("charts_config.json")
STANDARD_DATA_FILENAME = Path("data.gzip")
DASH_MOUNT_ROUTE = "/dash"
DASH_ROOT_ROUTE = DASH_MOUNT_ROUTE + "/"
MAX_NUMBER_FILTERS = 5


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


class DataTypes(str, BaseEnum):
    numerical = "numerical"
    categorical = "categorical"
