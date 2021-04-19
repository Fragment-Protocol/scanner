from base_types.network import Network


class BlockEvent:
    """
    Basic block event type.
    """
    def __init__(self, network: Network, **kwargs):
        self.network = network
        for key in kwargs.keys():
            self.__setattr__(key, kwargs[key])
