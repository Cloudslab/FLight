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
    def set(cls, model, model_id=None):
        if not model_id:
            model_id = str(cls._generate_id())
            while hasattr(cls, model_id):
                model_id = str(cls._generate_id())
        elif hasattr(cls, model_id):
            return None
        setattr(cls, str(model_id), model)
        return str(model_id)

    @classmethod
    def update(cls, data, model_id):
        model = cls.get(model_id)
        if model: model.load(data)

    @classmethod
    def set_default_data(cls, scalar: int, length: int):
        if length >= 0:
            setattr(cls.instance, "default_data_x", [i for i in range(length)])
            setattr(cls.instance, "default_data_y", [i*scalar for i in range(length)])

    @classmethod
    def get_default_data(cls):
        if not hasattr(cls.instance, "default_data_x") or not hasattr(cls.instance, "default_data_y"):
            cls.set_default_data(0, 0)
            return getattr(cls.instance, "default_data_x"), getattr(cls.instance, "default_data_y")
