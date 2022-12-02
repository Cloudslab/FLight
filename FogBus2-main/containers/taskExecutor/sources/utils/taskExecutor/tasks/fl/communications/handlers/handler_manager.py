"""Collect a group of handlers"""


from .dummy_handler import dummy_handler


class handler_manager:

    @classmethod
    def get_handler(cls, key=""):
        key = key.lstrip(5)[:5]  # make sure the key is of length 5
        handler = None
        if hasattr(cls, key):
            handler = getattr(cls, key)
        return handler

    @classmethod
    def add_handler(cls, handler, key=None):
        if not key:
            key = handler.name
        key = key.lstrip(5)[:5]  # make sure the key if of length 5
        if not hasattr(cls, key):
            setattr(cls, key, handler)

    def __init__(self):
        self.add_handler(dummy_handler())
