import questionary
from questionary import Choice

from src.wallets.create_evm_wallets import CreateEvmWallets

class WalletsManager:
    def __init__(self):
        self.wallets = []
    
    def show_menu(self):
        options = [
            Choice("查询钱包", "query_wallet"),
            Choice("新增已有钱包", "add_wallet"),
            Choice("批量创建钱包（会覆盖已有的钱包）", "create_wallets"),
            Choice("删除钱包", "delete_wallet"),
            Choice("退出", "back")
        ]

        user_choice = questionary.select("请选择您要的操作：", options).ask()

        if user_choice == "back":
            return
        
        # elif user_choice == "query_wallet":
        #     self.query_wallet()

        # elif user_choice == "add_wallet":
        #     self.add_wallet()
            
        elif user_choice == "create_wallets":
            CreateEvmWallets().run()

        # elif user_choice == "delete_wallet":
        #     self.delete_wallet()