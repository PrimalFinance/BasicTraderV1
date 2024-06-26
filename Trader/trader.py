from web3 import Web3


# Custom "Trader" periphery libraries.
from Trader.Periphery.abi import SYMBOL_ABI, pairabi, ethusdtabi
from Trader.Periphery.utils import Utils
from Trader.Periphery.token import TokenData, Token
from Trader.Periphery.dex import Dex


class Trader:
    def __init__(self, chain_id: int) -> None:
        self.chain_id = int(chain_id)
        self.utils = Utils()
        self.web3 = Web3(Web3.HTTPProvider(self.utils.get_rpc_url(chain_id)))

        # self.crypto.get_token_address("WETH", self.chain_id)
