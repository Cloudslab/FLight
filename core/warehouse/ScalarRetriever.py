from .RetrieverAbstract import RetrieverAbstract
from ..ml.basic.Scalar import Scalar
import uuid


class ScalarRetriever(RetrieverAbstract):

    RETRIEVER_NAMESPACE = "SCALAR"

    def get(self, unique_id: uuid.UUID) -> Scalar:
        if hasattr(self, unique_id) and isinstance(getattr(self, unique_id), Scalar):
            return getattr(self, unique_id)

        # ToDo: call debug logger here
        return None

    def set(self, unique_id: uuid.UUID, data: Scalar) -> bool:
        if not hasattr(self, unique_id):
            setattr(self, unique_id, data)

        else:
            getattr(self, unique_id).update(data.value)

        return True
