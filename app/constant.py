from enum import Enum, EnumMeta
from pathlib import Path

CHARTS_ROUTE = "/charts/"
TABLES_ROUTE = "/tables/"
STANDARD_CHARTS_CONFIG = Path("charts_config.yaml")
STANDARD_DATA_FILENAME = Path("data.gzip")
DASH_MOUNT_ROUTE = "/dash"
DASH_ROOT_ROUTE = DASH_MOUNT_ROUTE + "/"


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


class VisTypes(str, BaseEnum):
    bar = "bar"
    choropleth_map = "choropleth_map"
