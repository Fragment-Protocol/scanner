import os
import sys
import time
import logging
import traceback

from base_types.network import Network


class LastBlockPersister:
    """
    Class for write block numbers.
    """
    base_dir = 'block_numbers'

    def __init__(self, network: Network):
        self.network_name: str = network.type
        os.makedirs(self.base_dir, exist_ok=True)

    def get_last_block(self) -> int:
        try:
            with open(os.path.join(self.base_dir, self.network_name), 'r') as file:
                last_block_number = file.read()
        except FileNotFoundError:
            return 1
        return int(last_block_number)

    def save_last_block(self, last_block_number: int):
        with open(os.path.join(self.base_dir, self.network_name), 'w') as file:
            file.write(str(last_block_number))


class Scanner:
    """
    Basic scanner type.
    """
    INFO_INTERVAL = 60000
    WARN_INTERVAL = 120000

    def __init__(self, network: Network, last_block_persister: LastBlockPersister, polling_interval: int,
                 commitment_chain_length: int, reach_interval: int = 0):

        self.network = network
        self.last_block_persister = last_block_persister
        self.polling_interval = polling_interval
        self.commitment_chain_length = commitment_chain_length
        self.reach_interval = reach_interval

    def process_block(self, block):
        """
        The method for writing block processing logic.
        """
        raise NotImplementedError("WARNING: Function process_block must be overridden.")

    def poller(self):
        self.last_block_time = time.time()
        self.next_block_number = self.last_block_persister.get_last_block()
        logging.info('hello from {}'.format(self.network.type))

        while True:
            self.polling()

    def polling(self):
        try:
            self.last_block_number = self.network.get_last_block()

            if self.last_block_number - self.next_block_number > self.commitment_chain_length:
                logging.info('{}: Process next block {}/{} immediately.'.format(self.network.type, self.next_block_number,
                                                                         self.last_block_number))
                self.load_next_block()
                time.sleep(self.reach_interval)
                return

            time_interval = self.last_block_time - time.time()
            if time_interval > self.WARN_INTERVAL:
                logging.info('{}: there is no block from {} seconds!'.format(self.network.type, time_interval))
            elif time_interval > self.INFO_INTERVAL:
                logging.info('{}: there is no block from {} seconds.'.format(self.network.type, time_interval))

            # pending transactions logic

            logging.info('{}: all blocks processed, wait new one.'.format(self.network.type))
        except Exception:
            logging.info('{}: exception handled in polling cycle. Continue.'.format(self.network.type))
            logging.info('\n'.join(traceback.format_exception(*sys.exc_info())))

        time.sleep(self.polling_interval)

    def load_next_block(self):
        """
        The method for writing block numbers.
        """
        block = self.network.get_block(self.next_block_number)

        self.last_block_persister.save_last_block(self.next_block_number)
        self.next_block_number += 1
        self.last_block_time = time.time()

        self.process_block(block)
