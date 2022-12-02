"""
Contains:
1. uuid(string): unique id to identify a model
2. address: contact address to the model
"""


class model_pointer:
    def __init__(self, uuid, address):
        self.uuid = uuid
        self.address = address

    def __eq__(self, other):
        return self.uuid == other.uuid and self.address[0] == other.address[0]  # only check for IP similarity
