"""
class provide getter & setter for model retrieval from different storage media

"""
from enum import Enum
from .Accessory import *


class model_warehouse:
    class model_accessory_name(Enum):
        ram = 1
        local_file = 2
        ftp = 3

    def __init__(self):
        self.id_to_storage = {}
        self._ram_storage = ram_accessory()
        self._local_file_storage = local_file_accessory()
        self._ftp_server_storage = None

    def start_ftp_server(self, addr=("127.0.0.1", 12345)):
        self._ftp_server_storage = ftp_accessory(addr)

    def download_model(self, ftp_server_addr, server_file_name, user_name, password, data_id: str = None):
        self._local_file_storage.download_from_ftp(ftp_server_addr, server_file_name, user_name, password, data_id)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, data, model_id: str, storage: model_accessory_name):
        result_model_id = None
        if storage == self.model_accessory_name.ram:
            result_model_id = self._ram_storage.set({"model": data}, model_id)
            self.id_to_storage[result_model_id] = self.model_accessory_name.ram
        if storage == self.model_accessory_name.local_file:
            if type(data) is dict and "file_name" in data and "raw_data" in data:
                result_model_id = self._local_file_storage.set(data, model_id)
                self.id_to_storage[result_model_id] = self.model_accessory_name.local_file
        if storage == self.model_accessory_name.ftp and self._ftp_server_storage:
            if type(data) is dict and "file_name" in data and "raw_data" in data:
                result_model_id = self._ftp_server_storage.set(data, model_id)
                self.id_to_storage[result_model_id] = self.model_accessory_name.ftp
        return result_model_id

    def get_model(self, model_id: str):
        storage = self.id_to_storage.get(model_id, None)
        if storage == self.model_accessory_name.ram:
            return self._ram_storage.get({}, model_id)
        if storage == self.model_accessory_name.local_file:
            return self._local_file_storage.get({}, model_id)
        if storage == self.model_accessory_name.ftp:
            return self._ftp_server_storage.get({}, model_id)


model_storages_str = {"ram": model_warehouse.model_accessory_name.ram,
                      "local_file": model_warehouse.model_accessory_name.local_file,
                      "ftp": model_warehouse.model_accessory_name.ftp}
