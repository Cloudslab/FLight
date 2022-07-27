from abc import ABC, abstractmethod


class base_handler(ABC):

    @abstractmethod
    def __call__(self, conn, addr, tunnel):
        raise NotImplementedError("Handle logic should be rewrite")
