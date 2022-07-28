"""
Data-warehouse is an interface between actual model storage and federated learning logic.

A simple model maybe just store on RAM while a larger model may be store on file etc.

The '''get''' function should provide all necessary retrieval information and '''set''' function should create
a model in data-warehouse. Overload get/set to fit your own model.

'''update''' should connect with model load function: base_model::def load(self, data), overload load to achieve
different update method

"""

import uuid


class data_warehouse:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(data_warehouse, cls).__new__(cls)
        return cls.instance

    @classmethod
    def _generate_id(cls):
        return uuid.uuid1()

    @classmethod
    def get(cls, model_id):
        if hasattr(cls, str(model_id)):
            return getattr(cls, model_id)
        return None

    @classmethod
    def set(cls, data, model_id=None):
        if not model_id:
            model_id = str(cls._generate_id())
            while hasattr(cls, model_id):
                model_id = str(cls._generate_id())
        elif hasattr(cls, model_id):
            return None
        setattr(cls, str(model_id))
        return str(model_id)

    @classmethod
    def update(cls, data, model_id):
        model = cls.get(model_id)
        if model: model.load(data)