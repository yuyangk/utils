import pytest

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

from downloaders.gfs_downloader import GfsRealtimeDownloader
from downloaders.const import TCRI_PARAMETERS


def get_savepath(root_path: str, init_time: datetime, fcst_hour: int) -> Path:
    save_dir = Path(root_path, init_time.strftime("%Y/%m/%d/%H"))
    save_file = f"gfs.pgrb2.0p25.f{fcst_hour:03d}.{init_time.strftime('%y%m%d%H')}"
    return Path(save_dir, save_file)


def get_input_data():
    init_time = datetime(2024, 5, 20, 0)
    fcst_hour = 6
    save_root_path = "../data/"
    save_path = get_savepath(save_root_path, init_time, fcst_hour)
    request_params = TCRI_PARAMETERS
    return save_path, init_time, fcst_hour, request_params


@pytest.fixture
def gfs_downloader():
    save_path, init_time, fcst_hour, request_params = get_input_data()

    gfs_downloader = GfsRealtimeDownloader(
        save_path=save_path,
        init_time=init_time,
        fcst_hour=fcst_hour,
        request_params=request_params,
    )
    return gfs_downloader


def test_gfs_downloader_download_called_with_correct_parameters(gfs_downloader):
    # WIP to test if download is called with correct parameters
    pass


def test_download_gfs(gfs_downloader):
    gfs_downloader.download()

    save_path, _, _, _ = get_input_data()
    assert save_path.exists()
    assert save_path.stat().st_size > 0
