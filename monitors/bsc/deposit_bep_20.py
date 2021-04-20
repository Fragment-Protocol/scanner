from web3 import Web3, HTTPProvider

from contracts import factory
from settings import NETWORKS, CONTRACT_ADDRESS
from base_types import Block, Monitor, BlockEvent


class DepositBEP20(Monitor):
    event_type = "deposit_bep_20"

    def on_new_block_event(self, block_event: BlockEvent):
        w3 = Web3(HTTPProvider(NETWORKS[self.network_type]["url"]))
        contract = w3.eth.contract(
            address=Web3.toChecksumAddress(
                CONTRACT_ADDRESS[self.network_type]
            ),
            abi=factory,
        )
        block: Block = block_event.block
        event_filter = contract.events.DepositBEP20().createFilter(fromBlock=block.number, toBlock=block.number)
        events = event_filter.get_all_entries()

        if events:
            for event in events:
                message = dict(event["args"])
                self.send_to_backend(message=message)
