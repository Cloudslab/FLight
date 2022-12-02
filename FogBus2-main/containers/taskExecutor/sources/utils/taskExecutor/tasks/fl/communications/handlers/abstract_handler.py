"""
Abstract handler pattern that every other handler should follow

callable: __call__(self, conn, reply_addr, *args, **kwargs), conn(tcp connection object), reply_addr(place to reply)
"""

from abc import ABC, abstractmethod


class abstract_handler(ABC):

    EVENT_STRING_LEN = 10

    @abstractmethod
    def __call__(self, conn, reply_addr, *args, **kwargs):
        pass

