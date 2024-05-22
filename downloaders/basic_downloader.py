from pathlib import Path
import requests
import logging


class BasicDownloader:
    def __init__(
        self, download_url: str, save_path: str | Path, request_params: dict
    ) -> None:
        self.url = download_url
        self.save_path = Path(save_path)
        self.request_params = request_params

    def download(self):
        logging.debug("Downloading %s to %s", self.url, self.save_path)
        self._make_path()
        response = requests.get(self.url, params=self.request_params)
        self._save_file_with(response.content)
    
    def _save_file_with(self, content):
        with open(self.save_path, "wb") as file:
            file.write(content)

    def _make_path(self) -> None:
        # Create the directory if it doesn't exist
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
