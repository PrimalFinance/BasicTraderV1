import pandas as pd
from Trader.Periphery.constants import BASE_DATA_PATH
from web3 import Web3
from Trader.Periphery.abi import uniswap_factory_abi
from Trader.Periphery.utils import Utils


class Dex:
    def __init__(self, dex_name: str, dex_version: str, chain_id: int) -> None:

        self.pools_path = (
            f"{BASE_DATA_PATH}\\Pools\\{dex_name}{dex_version.upper()}.json"
        )
        self.dex_path = f"{BASE_DATA_PATH}\\Dexs\\dexs.json"
        self.name = dex_name
        self.version = dex_version.upper()
        self.chain_id = chain_id
        self.utils = Utils()

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
                            fee_tier
                        ]

                    else:
                        pool_address = self._fetch_pool_externally(
                            tokenA_address, tokenB_address, fee_tier
                        )
                        j[chain_id][tokenA_address][tokenB_address][
                            fee_tier
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
        utils = Utils()
        rpc_url = utils.get_rpc_url(self.chain_id)
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        print(f"Factory: {self.get_factory_address(self.chain_id)}")
        uniswap_factory = web3.eth.contract(
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

    def get_price(self):

        if self.version == "V2":
            self.priceV2()
        elif self.version == "V3":
            self.priceV3()

    def priceV2(self):
        pass

    def priceV3(self):
        pass

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
