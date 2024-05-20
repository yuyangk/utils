from datetime import datetime

from .basic_downloader import BasicDownloader
from const import NCEP_REALTIME_URL


class NcepRealtimeDownloader(BasicDownloader):
    def __init__(
        self, save_path: str, init_time: datetime, fcst_hour: int, **request_params
    ):
        super().__init__(
            download_url=NCEP_REALTIME_URL, save_path=save_path, **request_params
        )
        self.init_date = init_time.strftime("%Y%m%d")
        self.init_hour = init_time.strftime("%H")
        self.fcst_hour = fcst_hour

    def _get_parameters(self) -> dict:
        file_parameters = {
            "dir": f"/gfs.{self.init_date}/{self.init_hour}/atmos",
            "file": f"gfs.t{self.init_hour}z.pgrb2.0p25.f{self.fcst_hour:03d}",
        }
        parameters = {**file_parameters, **self.request_params}
        return parameters

    def ncep_download(self):
        parameters = self._get_parameters()
        self.download(**parameters)
