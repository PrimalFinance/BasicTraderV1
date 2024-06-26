import os
import json
from dotenv import load_dotenv

load_dotenv()


class Utils:
    def __init__(self) -> None:
        pass

    """---------------------------------"""

    def get_rpc_url(self, chainId):

        # Convert chainId to "int" if not already.
        chainId = int(chainId)

        if chainId == 1:
            url = os.getenv("INFURA_ETHEREUM_URL")
        elif chainId == 10:
            url = os.getenv("INFURA_OPTIMISM_URL")
        elif chainId == 137:
            url = os.getenv("INFURA_POLYGON_URL")

        elif chainId == 42161:
            url = os.getenv("INFURA_ARBITRUM_URL")

        return url

    """---------------------------------"""

    def read_json(self, path: str):
        if not os.path.exists(path):
            return {}
        with open(path, "r") as file:
            data = json.load(file)

        return data

    """---------------------------------"""

    def write_json(self, json_object, path: str):
        with open(path, "w") as file:
            json.dump(json_object, file, indent=4)

    """---------------------------------"""

    def display_json(self, json_object):
        print(json.dumps(json_object, indent=4))

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""

    """---------------------------------"""
