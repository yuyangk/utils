import pandas as pd
from .basic_writer import BasicWriter


class CsvWriter(BasicWriter):
    def __init__(self, path) -> None:
        super().__init__(path)

    def write(self, data: pd.DataFrame, **kwargs):
        self._make_path(self.path)
        data.to_csv(self.path, **kwargs)
