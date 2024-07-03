import pytest
from readers.grib_reader import GribReader

import logging

FORMAT = "%(asctime)s %(filename)s %(levelname)s:%(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


@pytest.fixture
def grib_reader():
    grib_reader = GribReader("./gfs.pgrb2.0p25.f006.24052000")
    return grib_reader


def test_open_file(grib_reader):
    file_index = grib_reader.open_file()
    logging.info(file_index)
    grib_reader.close_file(file_index)


def test_read_index(grib_reader):
    keys = ("name", "typeOfLevel", "level")
    file_index = grib_reader.read_index(*keys)
    logging.info(file_index)
    grib_reader.close_file(file_index)


def test_read_variable(grib_reader):
    keys = ("name", "typeOfLevel", "level")
    file_index = grib_reader.read_index(*keys)
    var_infos = {"name": "Temperature", "typeOfLevel": "isobaricInhPa", "level": 200}
    variable = grib_reader.read_variable(file_index, **var_infos)
    logging.info(variable)
    grib_reader.close_file(file_index)


def test_read(grib_reader):
    keys = ("name", "typeOfLevel", "level")
    var_infos = {"name": "Temperature", "typeOfLevel": "isobaricInhPa", "level": 200}
    variable = grib_reader.read(*keys, **var_infos)
    logging.info(variable)
