import datetime
import pytest
from unittest.mock import MagicMock
from downloader.gfs_downloader import NcepRealtimeDownloader


@pytest.fixture
def ncep_downloader():
    save_path = "./data"
    init_time = datetime.datetime(2021, 1, 1, 0)
    fcst_hour = 12
    request_params = {"request_param1": "value1", "request_param2": "value2"}
    return NcepRealtimeDownloader(save_path, init_time, fcst_hour, **request_params)


def test_ncep_downloader_download_called_with_correct_parameters(ncep_downloader):
    # Mock the download method
    mock_download = MagicMock()
    ncep_downloader.download = mock_download

    # Call the ncep_download method
    ncep_downloader.ncep_download()

    # Check that the download method was called with the correct parameters
    expected_parameters = {
        "dir": "/gfs.20210101/00/atmos",
        "file": "gfs.t00z.pgrb2.0p25.f012",
        "request_param1": "value1",
        "request_param2": "value2",
    }
    mock_download.assert_called_once_with(**expected_parameters)
