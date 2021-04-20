from web3 import Web3, HTTPProvider

from settings import NETWORKS
from contracts import exchange_from_ethereum
from base_types import Block, Monitor, BlockEvent, Transaction


class WithdrawNFT(Monitor):
    event_type = "withdraw_nft"

    def on_new_block_event(self, block_event: BlockEvent):
        w3 = Web3(HTTPProvider(NETWORKS[self.network_type]["url"]))
        contract = w3.eth.contract(
            address=Web3.toChecksumAddress(
                "0x938A1a961329772FebdF5e4Cea6830865b9b2c1C"
            ),
            abi=exchange_from_ethereum,
        )
        block: Block = block_event.block
        event_filter = contract.events.WithdrawNFT().createFilter(fromBlock=block.number, toBlock=block.number)
        events = event_filter.get_all_entries()

        if events:
            for event in events:
                self.send_to_backend(event["args"])
