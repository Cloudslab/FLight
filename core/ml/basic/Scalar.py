"""
A single number
"""


class Scalar:
    __slots__ = ["value", "version"]

    def __init__(self, value):
        self.value = value
        self.version = 1

    def update(self, new_value):
        self.value = new_value
        self.version += 1
