import typing

from base_types.output import Output


class Transaction:
    """
    Basic transaction type.
    """
    def __init__(self, tx_hash: str, inputs: typing.List[str], outputs: typing.List[Output],
                 contract_creation: bool, creates: str):
        self.tx_hash = tx_hash
        self.inputs = inputs
        self.outputs = outputs
        self.contract_creation = contract_creation
        self.creates = creates
