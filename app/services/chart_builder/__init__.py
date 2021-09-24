from abc import ABC, abstractmethod


class ChartBuilderInterface(ABC):
    @abstractmethod
    def validate_columns(self):
        pass

    @abstractmethod
    def build_chart(self):
        pass
