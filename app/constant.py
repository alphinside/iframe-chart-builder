from enum import Enum, EnumMeta

CHARTS_ROUTE = "/charts"
TABLES_ROUTE = "/tables"


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
    table = "table"
    bar = "bar"
    choropleth_map = "choropleth_map"
