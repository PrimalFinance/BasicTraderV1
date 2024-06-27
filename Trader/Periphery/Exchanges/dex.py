import pandas as pd
from Trader.Periphery.Constants.constants import BASE_DATA_PATH
from web3 import Web3
from Trader.Periphery.Constants.abi import uniswap_factory_abi, uniswapV3_pool_abi
from Trader.Periphery.Utils.utils import Utils


class Dex:
    def __init__(
        self, dex_name: str, dex_version: str, chain_id: int, debug: bool = True
    ) -> None:

        self.pools_path = (
            f"{BASE_DATA_PATH}\\Pools\\{dex_name}{dex_version.upper()}.json"
        )
        self.dex_path = f"{BASE_DATA_PATH}\\Dexs\\dexs.json"
        self.name = dex_name
        self.version = dex_version.upper()
        self.chain_id = chain_id
        self.debug = debug
        self.utils = Utils()
        rpc_url = self.utils.get_rpc_url(self.chain_id)
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

        self.available_fee_tiers = [100, 500, 3000, 10000]

    """---------------------------------"""

    def get_pool_address(
        self,
        tokenA_address,
        tokenB_address,
        fee_tier: int,
    ):
        chain_id = str(self.chain_id)

        tokenA_address = Web3.to_checksum_address(tokenA_address)
        tokenB_address = Web3.to_checksum_address(tokenB_address)

        data = {}

        j = self.utils.read_json(self.pools_path)
        if str(self.chain_id) in j.keys():
            if tokenA_address in j[str(self.chain_id)].keys():
                if tokenB_address in j[str(self.chain_id)][tokenA_address].keys():
                    if (
                        str(fee_tier)
                        in j[str(self.chain_id)][tokenA_address][tokenB_address].keys()
                    ):
                        pool_address = j[chain_id][tokenA_address][tokenB_address][
                            str(fee_tier)
                        ]

                    else:
                        pool_address = self._fetch_pool_externally(
                            tokenA_address, tokenB_address, fee_tier
                        )
                        j[chain_id][tokenA_address][tokenB_address][
                            str(fee_tier)
                        ] = pool_address
                        self.utils.write_json(j, self.pools_path)

                else:
                    pool_address = self._fetch_pool_externally(
                        tokenA_address, tokenB_address, fee_tier
                    )
                    j[chain_id][tokenA_address][tokenB_address] = {
                        f"{fee_tier}": pool_address
                    }
                    self.utils.write_json(j, self.pools_path)

            else:
                pool_address = self._fetch_pool_externally(
                    tokenA_address, tokenB_address, fee_tier
                )
                j[chain_id][tokenA_address] = {
                    f"{tokenB_address}": {f"{fee_tier}": pool_address}
                }
                self.utils.write_json(j, self.pools_path)

        else:
            pool_address = self._fetch_pool_externally(
                tokenA_address, tokenB_address, fee_tier
            )
            j[chain_id] = {
                f"{tokenA_address}": {
                    f"{tokenB_address}": {f"{fee_tier}": pool_address}
                }
            }
            self.utils.write_json(j, self.pools_path)

        return pool_address

    """---------------------------------"""

    def _fetch_pool_externally(self, tokenA_address, tokenB_address, fee_tier):
        if self.debug:
            print(f"[Factory Address Used]: {self.get_factory_address(self.chain_id)}")
        uniswap_factory = self.web3.eth.contract(
            address=self.get_factory_address(self.chain_id), abi=uniswap_factory_abi
        )

        pool_address = uniswap_factory.functions.getPool(
            tokenA_address, tokenB_address, fee_tier
        ).call()
        return pool_address

    """---------------------------------"""

    def get_factory_address(self, chain_id: str):
        if type(chain_id) != type(str):
            chain_id = str(chain_id)
        df = pd.read_json(self.dex_path)
        factory_address = df[self.name][self.version][chain_id]["factoryAddress"]
        return factory_address

    """---------------------------------"""

    def get_price(self, token_in, token_out):

        if self.version == "V2":
            self.priceV2()
        elif self.version == "V3":
            price = self.priceV3(token_in, token_out)
        return price

    def priceV2(self):
        pass

    def priceV3(self, token_in, token_out):
        pool_address = self.get_pool_address(token_in.address, token_out.address, 500)
        if self.debug:
            print(f"[Pool Address Used]: {pool_address}")
        pool_contract = self.web3.eth.contract(
            address=pool_address, abi=uniswapV3_pool_abi
        )
        # Fetch slot0 data
        slot0 = pool_contract.functions.slot0().call()

        # Extract sqrtPriceX96
        sqrtPriceX96 = slot0[0]

        if token_in.address > token_out.address:
            decimals_diff = token_in.decimals - token_out.decimals
            price = (sqrtPriceX96 / 2**96) ** 2 / (10**decimals_diff)
            price = 1 / price
        else:
            decimals_diff = token_in.decimals - token_out.decimals
            price = (sqrtPriceX96 / 2**96) ** 2 * (10**decimals_diff)

        return price

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
