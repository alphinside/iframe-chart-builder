from abc import ABC, abstractmethod

import pandas as pd
from plotly.graph_objs._figure import Figure

from app.schema.requests import ChartBuilderRequest


class ChartBuilderInterface(ABC):
    def __init__(self, params: ChartBuilderRequest):
        self.output_path = params.output_path
        self.title = params.title
        self.graph_params = params.graph_params

        df = pd.read_excel(params.input_path)
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
