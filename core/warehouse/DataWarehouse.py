import uuid

from .RetrieverAbstract import RetrieverAbstract
from .ScalarRetriever import ScalarRetriever
from .ModelWarehouse import ModelRetriever

class DataWarehouse:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(DataWarehouse, cls).__new__(cls)
            cls.instance.__setattr__(ScalarRetriever.RETRIEVER_NAMESPACE, ScalarRetriever())
            cls.instance.__setattr__(ModelRetriever.RETRIEVER_NAMESPACE, ModelRetriever())
        return cls.instance

    @classmethod
    def _generate_id(cls):
        return uuid.uuid1()

    @classmethod
    def add_retriever(cls, retriever_name, retriever: RetrieverAbstract):
        if not hasattr(cls, retriever_name):
            setattr(cls, retriever_name, retriever)

    @classmethod
    def get(cls, retriever_name, unique_id: uuid.UUID):
        if not hasattr(cls.instance, retriever_name):
            # ToDo: call debug logger
            return None
        if not isinstance(getattr(cls.instance, retriever_name), RetrieverAbstract):
            # ToDo: call debug logger
            return None

        return getattr(cls.instance, retriever_name).get(str(unique_id))

    @classmethod
    def set(cls, retriever_name, data, unique_id: uuid.UUID = None):
        if not hasattr(cls.instance, retriever_name):
            # ToDo: call debug logger
            return None
        if not isinstance(getattr(cls.instance, retriever_name), RetrieverAbstract):
            # ToDo: call debug logger
            return None

        new_id = str(unique_id) if unique_id else str(cls._generate_id())
        if getattr(cls.instance, retriever_name).set(new_id, data):
            return new_id
        else:
            return None
