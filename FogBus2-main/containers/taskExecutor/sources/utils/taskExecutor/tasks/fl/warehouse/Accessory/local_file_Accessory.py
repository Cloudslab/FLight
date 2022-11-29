"""This file represents data stored on local files"""

from .abstract_Accessory import abstract_accessory
from collections import defaultdict
from ..storage_folder.folder_manager import folder_position
import os
import pickle

class local_file_accessory(abstract_accessory):
    def __init__(self):
        self._file_paths = defaultdict(lambda: "")
        self._destination_folder = folder_position.local_file_storage_folder()

    def get(self, args: dict, data_id: str):
        file_path = self._file_paths.get(data_id)
        if file_path:
            return self.read_from_file(file_path)
        else:
            return None

    # args are expected to contain file_name (file name & extensions) & raw_data to be written into the file
    def set(self, args: dict, data_id: str = None):
        if not data_id:
            data_id = self.get_new_id()
        if "file_name" in args and "raw_data" in args:
            file_path = os.path.join(self._destination_folder, args["file_name"])
            self.write_to_file(file_path, args["raw_data"])
            self._file_paths[data_id] = file_path
        return data_id

    @staticmethod
    def write_to_file(file_path, data):
        f = open(file_path, "wb+")
        f.write(pickle.dumps(data))
        f.close()

    @staticmethod
    def read_from_file(file_path):
        f = open(file_path, "rb")
        data = pickle.loads(f.read())
        f.close()
        return data


