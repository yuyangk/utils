import pygrib as pb
from .basic_reader import BasicReader


class GribReader(BasicReader):
    def __init__(self, file_fullname: str) -> None:
        self.check_file_exist(file_fullname)
        self.file = file_fullname

    def read(self, *index, **var_infos):
        file_index = self.read_index(*index)
        return self.read_variable(file_index, **var_infos)

    def open_file(self):
        return pb.open(self.file)

    def read_index(self, *keys):
        return pb.index(self.file, *keys)

    def read_variable(self, file_index, **var_infos):
        return file_index.select(**var_infos)[0]

    def close_file(self, file_index) -> None:
        file_index.close()

    def show_variables(self) -> None:
        with pb.open(self.file) as file:
            print(file.select())

    def get_variable_attribute(self, variable, attribute_name: str):
        return variable[attribute_name]
