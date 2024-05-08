import config
import security

import questionary
from questionary import Choice, Separator

from src.wallets.create_evm_wallets import CreateEvmWallets
from src.wallets.get_gas_price import GetGasPrice
from src.apps.uniswap.uniswap_v3 import UniswapV3

MENU = [
    Choice("创建 EVM 钱包", "create_evm_wallet"),
    Choice("获取 gas 价格", "get_gas_price"),
    Separator(),
    Choice("Uniswap ", "uniswap"),
    Choice("退出程序", "exit")
]

def main():
    # 准备工作目录
    config.setup()
    security.setup()

    # 菜单
    while True:
        user_choice = questionary.select("你想做什么？", choices=MENU).ask()

        if user_choice == "create_evm_wallet":
            CreateEvmWallets().run()

        elif user_choice == "get_gas_price":
            GetGasPrice().get_gas_price()

        elif user_choice == "uniswap":
            UniswapV3().showMenu()

        # 退出
        elif user_choice == None or user_choice == "exit":
            print("再见！")
            exit()


if __name__ == "__main__":
    main()
