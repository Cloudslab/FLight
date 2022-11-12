"""
class provide getter & setter for training data retrieval from different storage media

"""


class data_warehouse:
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(data_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_data(self, data, data_id: str = None, storage: str = None):
        pass

    def get_data(self, data_id: str):
        pass
