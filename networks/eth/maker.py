from networks.eth.scanner import EthScanner
from networks.eth.network import EthNetwork
from base_types.scanner import LastBlockPersister


class EthMaker:
    def __init__(
        self, network_name: str, polling_interval: int, commitment_chain_length: int
    ):
        network = EthNetwork(network_name)
        last_block_persister = LastBlockPersister(network)
        self.scanner = EthScanner(
            network, last_block_persister, polling_interval, commitment_chain_length
        )
