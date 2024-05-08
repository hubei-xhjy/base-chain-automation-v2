from config import WALLET_DIR, WALLET_BACKUP_DIR
from security import encrypt

from datetime import datetime

from mnemonic import Mnemonic
from eth_account import Account
from eth_account.signers.local import LocalAccount

from tqdm.rich import trange
import warnings
from tqdm import TqdmExperimentalWarning
import questionary


class CreateEvmWallets():
    def __init__(self):
        warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
        Account.enable_unaudited_hdwallet_features()
        self.mnemonic_generator = Mnemonic("english")
        self.account_list = ['id,address,private_key,mnemonic']
        self.current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        self.wallet_count = 100
        self.save_file_path = f'{WALLET_DIR}/wallets.bin'
        self.save_file_bak_path = f'{WALLET_BACKUP_DIR}/wallets_{self.current_time}.bin'
    

    def generate_wallets(self):
        """生成钱包 + 密钥 + 助记词"""
        for id in trange(self.wallet_count):
            mnemo = self.mnemonic_generator.generate(strength=128)
            account: LocalAccount = Account.from_mnemonic(mnemo)
            account_detail = f"{id},{account.address},{account.key.hex()},{mnemo}"
            self.account_list.append(account_detail)
        
    
    def save_wallets(self):
        """将钱包加密并保存在 CSV 文件中"""
        content = "\n".join(self.account_list)
        encrypted_content = encrypt(content)

        with open(self.save_file_path, 'wb') as f:  # 注意使用二进制写入模式 'wb'
            f.write(encrypted_content)

        with open(self.save_file_bak_path, 'wb') as f:  # 同上使用二进制写入模式
            f.write(encrypted_content)
    
    def run(self):
        # 获取生成钱包的数量
        self.wallet_count = questionary.text(
            "请输入您想生成的钱包数量：", validate=lambda cnt: cnt.isdigit()).ask()
        self.wallet_count = int(self.wallet_count) if self.wallet_count else 0  # 默认生成 100 个钱包

        print(f"准备生成 {self.wallet_count} 个钱包...")

        if self.wallet_count == 0:
            print("用户取消操作")
            return

        # 生成和保存钱包
        print("钱包和助记词生成中...")
        self.generate_wallets()
        self.save_wallets()
        print("钱包信息已经加密保存到：{} 中。".format(self.save_file_path))