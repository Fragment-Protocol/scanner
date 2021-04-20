from web3 import Web3, HTTPProvider

from contracts import exchange_from_ethereum
from settings import NETWORKS, CONTRACT_ADDRESS
from base_types import Block, Monitor, BlockEvent


class DepositNFT(Monitor):
    event_type = "deposit_nft"

    def on_new_block_event(self, block_event: BlockEvent):
        w3 = Web3(HTTPProvider(NETWORKS[self.network_type]["url"]))
        contract = w3.eth.contract(
            address=Web3.toChecksumAddress(
                CONTRACT_ADDRESS[self.network_type]
            ),
            abi=exchange_from_ethereum,
        )
        block: Block = block_event.block
        event_filter = contract.events.DepositNFT().createFilter(fromBlock=block.number, toBlock=block.number)
        events = event_filter.get_all_entries()

        if events:
            for event in events:
                self.send_to_backend(event["args"])
