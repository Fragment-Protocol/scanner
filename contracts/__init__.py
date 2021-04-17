"""
Contain contract ABIs in json format.
For each contract, the events of which the scanner must catch, you need to add ABI here.
"""
import json


def _open_abi(name):
    with open(f"contracts/{name}.json") as f:
        result = json.load(f)
    return result


factory = _open_abi("factory")
exchange_from_ethereum = _open_abi("exchange_from_ethereum")
