from web3 import Web3
from config import getBaseRpc

class GetGasPrice:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(getBaseRpc()))

    def get_gas_price(self):
        # 获取当前的gas价格
        gas_price = self.w3.eth.gas_price
        print("当前的gas价格为:", gas_price)
