import uuid
from abc import ABC, abstractmethod


class RetrieverAbstract(ABC):

    @abstractmethod
    def get(self, unique_id: uuid.UUID):
        raise NotImplementedError("This function should return data based on uuid.",
                                  "Failure should be bounded and return None.")

    @abstractmethod
    def set(self, unique_id: uuid.UUID, data) -> bool:
        raise NotImplementedError("This function should store data corresponds to uuid. Indicate if insert access.")
