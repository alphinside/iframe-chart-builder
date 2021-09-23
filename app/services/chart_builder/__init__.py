from abc import ABC, abstractmethod
from pathlib import PosixPath

from plotly.graph_objs._figure import Figure


class ChartBuilderInterface(ABC):
    @abstractmethod
    def validate_columns(self):
        pass

    @abstractmethod
    def build_chart(self):
        pass

    def dump_to_html(self, fig: Figure, output_path: PosixPath):
        fig.write_html(output_path)
