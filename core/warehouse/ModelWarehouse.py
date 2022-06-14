from .RetrieverAbstract import RetrieverAbstract
from ..ml.model.Model import Model
import uuid


class ModelRetriever(RetrieverAbstract):

    RETRIEVER_NAMESPACE = "MODEL"

    def get(self, unique_id: uuid.UUID):
        if hasattr(self, unique_id) and isinstance(getattr(self, unique_id), Model):
            return getattr(self, unique_id)

        # ToDo: call debug logger here
        return None

    def set(self, unique_id: uuid.UUID, model) -> bool:
        if not hasattr(self, unique_id):
            setattr(self, unique_id, model)

        else:
            pass
            # ToDo, here I will just call the update function of model itself, later should be generalized here

        return True
