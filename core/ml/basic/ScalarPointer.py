from ..Pointer import Pointer
from Scalar import Scalar
from ...communication.utils.types import Address
from ...warehouse.ScalarRetriever import ScalarRetriever

"""
After a Scalar is created, this is produced to pass to remote to provide access
"""


class ScalarPointer(Pointer):

    def __init__(self, scalar: Scalar, address: Address, unique_id: int):
        Pointer.__init__(address, unique_id, scalar.version, ScalarRetriever.RETRIEVER_NAMESPACE)
