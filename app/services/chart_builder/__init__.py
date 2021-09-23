from abc import ABC, abstractmethod
from pathlib import PosixPath

import pandas as pd
from plotly.graph_objs._figure import Figure


class ChartBuilderInterface(ABC):
    def __init__(self, output_path: PosixPath, input_path: PosixPath):
        self.output_path = output_path

        df = pd.read_excel(input_path)
        self.df = df.loc[:, ~df.columns.str.match("Unnamed")].copy()

    @abstractmethod
    def validate_columns(self):
        pass

    @abstractmethod
    def build_chart(self):
        pass

    def dump_to_html(self, fig: Figure):
        self.output_path.parent.mkdir(exist_ok=True)

        fig.write_html(self.output_path)
