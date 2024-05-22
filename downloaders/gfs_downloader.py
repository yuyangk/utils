from datetime import datetime
from pathlib import Path

from .basic_downloader import BasicDownloader
from .const import GFS_REALTIME_URL


class GfsRealtimeDownloader(BasicDownloader):
    def __init__(
        self,
        save_path: str | Path,
        init_time: datetime,
        fcst_hour: int,
        request_params: dict = {},
    ):
        self.init_date = init_time.strftime("%Y%m%d")
        self.init_hour = init_time.strftime("%H")
        self.fcst_hour = fcst_hour

        all_params = self._get_all_parameters(request_params)

        super().__init__(
            download_url=GFS_REALTIME_URL,
            save_path=save_path,
            request_params=all_params,
        )

    def _get_file_params(self):
        file_parameters = {
            "dir": f"/gfs.{self.init_date}/{self.init_hour}/atmos",
            "file": f"gfs.t{self.init_hour}z.pgrb2.0p25.f{self.fcst_hour:03d}",
        }
        return file_parameters

    def _get_all_parameters(self, request_params: dict) -> dict:
        _file_params = self._get_file_params()
        all_params = {**_file_params, **request_params}
        return all_params

    # def gfs_download(self):
    #    parameters = self._get_parameters()
    #    self.download(parameters)
