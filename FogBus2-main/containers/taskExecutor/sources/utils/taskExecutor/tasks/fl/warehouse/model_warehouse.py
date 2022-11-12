"""
class provide getter & setter for model retrieval from different storage media

"""


class model_warehouse:
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            setattr(cls, "instance", super(model_warehouse, cls).__new__(cls))
        return getattr(cls, "instance")

    def set_model(self, data, model_id: str = None, storage: str = None):
        pass

    def get_model(self, model_id: str):
        pass
