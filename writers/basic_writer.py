import abc
from pathlib import Path


class BasicWriter(metaclass=abc.ABCMeta):
    def __init__(self, path) -> None:
        self.path = path

    @abc.abstractmethod
    def write(self, data):
        pass

    def _make_path(self, save_path: Path) -> None:
        # Create the directory if it doesn't exist
        save_path.parent.mkdir(parents=True, exist_ok=True)
