import json
import logging

import pika

from settings import NETWORKS


class Monitor:
    network_type: str
    event_type: str
    queue: str

    def __init__(self, network):
        self.network_type = network
        self.queue = NETWORKS[self.network_type]["queue"]

    def process(self, block_event):
        if block_event.network.type != self.network_type:
            return

        self.on_new_block_event(block_event)

    def on_new_block_event(self, block_event):
        raise NotImplementedError(
            "WARNING: Function on_new_block_event must be overridden."
        )

    def send_to_backend(self, message: dict):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                "localhost",
                5672,
                "rabbit",
                pika.PlainCredentials("rabbit", "rabbit"),
            )
        )
        channel = connection.channel()
        channel.queue_declare(
            queue=self.queue, durable=True, auto_delete=False, exclusive=False
        )
        channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(type=self.event_type),
        )
        connection.close()

        logging.info("{} sent message to backend: {}".format(self.__class__.__name__, message))
