NETWORKS = {
    'ETHEREUM_MAINNET': {
        'url': 'https://rinkeby.infura.io/v3/abe728c92de947c9ad3511189da14459',
        'polling_interval': 10,
        'commitment_chain_length': 5,
        'queue': 'notification-ethereum',
        'remove_middleware': True,
    },
    'BSC_MAINNET': {
        'url': 'https://data-seed-prebsc-1-s1.binance.org:8545/',
        'polling_interval': 10,
        'commitment_chain_length': 5,
        'queue': 'notification-bsc',
        'remove_middleware': True,
    },
}
MONITORS = {
    "DepositNFT": "ETHEREUM_MAINNET",
    "WithdrawNFT": "ETHEREUM_MAINNET",

    "TokenCreated": "BSC_MAINNET",
    "DepositBEP20": "BSC_MAINNET",
    "IsReadyToWithdraw": "BSC_MAINNET",
}
