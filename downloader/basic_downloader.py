from pathlib import Path
import requests


class BasicDownloader:
    def __init__(self, download_url: str, save_path: str, **request_params) -> None:
        self.url = download_url
        self.save_path = Path(save_path)
        self.request_params = request_params

    def download(self):
        self._make_path()
        with open(self.save_path, "wb") as file:
            # Pass the request_params to requests.get
            file.write(requests.get(self.url, **self.request_params).content)

    def _make_path(self) -> None:
        # Create the directory if it doesn't exist
        self.save_path.parent.mkdir(parents=True, exist_ok=True)
