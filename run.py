import threading

from pubsub import pub

import monitors
from networks import scanner_makers
from settings import NETWORKS, MONITORS

subscribe_list = []
for name, network in MONITORS.items():
    monitor_class = getattr(monitors, name, None)
    if monitor_class:
        monitor = monitor_class(network)
        subscribe_list.append((monitor.process, network))
    else:
        raise ImportWarning(f'WARNING: Monitor {name} not found. Check config.yaml file.')

# pubsub lib do not remember variables, created inside loop.
# So, we create list of variables in one loop, and then push it to pubsub
for elem in subscribe_list:
    pub.subscribe(*elem)


class ScanEntrypoint(threading.Thread):

    def __init__(self, network_maker, network_name, polling_interval, commitment_chain_length):
        super().__init__()
        self.network = network_maker(network_name, polling_interval, commitment_chain_length)

    def run(self):
        self.network.scanner.poller()


# Running scanner
if __name__ == "__main__":
    for net_name, net_info in NETWORKS.items():
        maker_names = scanner_makers.keys()
        for maker_name in maker_names:
            maker = scanner_makers[maker_name]
            scan = ScanEntrypoint(
                maker,
                net_name,
                net_info["polling_interval"],
                net_info["commitment_chain_length"],
            )
            scan.start()
