"""Collect a group of handlers"""


from .abstract_handler import abstract_handler
from .dummy_handler import dummy_handler
from .relationship_handler import relationship_handler
from .training_handlers import training_handler
from .model_communication_handlers import model_communication_handler
handler_name_len = abstract_handler.HANDLER_NAME_LENGTH


class handler_manager:
    INITIALIZED = False
    @classmethod
    def get_handler(cls, key=""):
        if not handler_manager.INITIALIZED:
            handler_manager()
        key = key.ljust(handler_name_len)[:handler_name_len]  # make sure the key is of length handler_name_len
        handler = None
        if hasattr(cls, key):
            handler = getattr(cls, key)
        return handler

    @classmethod
    def add_handler(cls, handler, key=None):
        if not key:
            key = handler.name
        key = key.ljust(handler_name_len)[:handler_name_len]  # make sure the key if of length handler_name_len
        if not hasattr(cls, key):
            setattr(cls, key, handler)

    def __init__(self):
        self.add_handler(dummy_handler())
        self.add_handler(relationship_handler())
        self.add_handler(training_handler())
        self.add_handler(model_communication_handler())

