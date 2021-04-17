from web3 import Web3
from hexbytes import HexBytes
from web3.middleware import geth_poa_middleware

from settings import NETWORKS
from base_types import Block, Network, Output, Transaction, TransactionReceipt


class EthNetwork(Network):

    def __init__(self, type):
        super().__init__(type)
        config = NETWORKS[type]

        urls = config['url']
        if not isinstance(urls, list):
            urls = [urls]
        for url in urls:
            rpc = Web3(Web3.HTTPProvider(url))
            # Disable ethereum special checks, if network used for non-eth chain
            if config.get('remove_middleware'):
                rpc.middleware_onion.inject(geth_poa_middleware, layer=0)
            self.add_rpc(rpc)

    def get_last_block(self):
        return self.rpc.eth.blockNumber

    def get_block(self, number: int) -> Block:
        block = self.rpc.eth.getBlock(number, full_transactions=True)
        block = Block(
            block['hash'].hex(),
            block['number'],
            block['timestamp'],
            [self._build_transaction(t) for t in block['transactions']],
        )

        return block

    @staticmethod
    def _build_transaction(tx):
        tx_hash = tx['hash']
        if isinstance(tx_hash, HexBytes):
            tx_hash = tx_hash.hex()

        output = Output(
            tx_hash,
            0,
            tx['to'],
            tx['value'],
            tx['input']
        )

        # Field 'to' is empty when tx creates contract
        contract_creation = tx['to'] is None
        tx_creates = tx.get('creates', None)

        # 'creates' is None when tx dont create any contract
        t = Transaction(
            tx_hash,
            [tx['from']],
            [output],
            contract_creation,
            tx_creates
        )
        return t

    def get_tx_receipt(self, hash):
        tx_res = self.rpc.eth.getTransactionReceipt(hash)
        return TransactionReceipt(
            tx_res['transactionHash'].hex(),
            tx_res['contractAddress'],
            tx_res['logs'],
            bool(tx_res['status']),
        )
