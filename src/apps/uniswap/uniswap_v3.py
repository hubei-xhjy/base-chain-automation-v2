from web3 import Web3
from config import getBaseRpc
import questionary
from questionary import Choice, Separator
from cprint import cprint


class UniswapV3:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(getBaseRpc()))
        self.current_chain = "base"
        with open(f"abi/uniswap_v3_abi.json", "r") as f:
            self.pool_abi = "".join(f.readlines())
        with open(f"abi/erc20_token_abi.json", "r") as f:
            self.erc20_token_abi = "".join(f.readlines())

    def showMenu(self):
        while True:
            pool_pair_address = questionary.select("请选择你要的操作的交易对：", [
                Choice("WETH / USDC ",
                       "0xd0b53d9277642d899df5c87a3966a349a798f224"),
                Choice("WETH / DEGEN",
                       "0xc9034c3e7f58003e6ae0c8438e7c8f4598d5acaa"),
                Choice("WETH / $mfer",
                       "0x7ec18abf80e865c6799069df91073335935c4185"),
                Choice("BALD / WETH ",
                       "0x9e37cb775a047ae99fc5a24dded834127c4180cd"),
                Choice("WETH / BORED",
                       "0xcfaf75a3d292c3535ea3acdb16ed2ee58c2bb091"),
                Choice("WETH / AERO ",
                       "0x3d5d143381916280ff91407febeb52f2b60f33cf"),
                Separator(),
                Choice("返回", "back")
            ]).ask()

            if pool_pair_address == "back":
                return
            elif str(pool_pair_address).startswith("0x"):
                pool_pair_address = self.w3.to_checksum_address(
                    pool_pair_address)
                self.getPairData(pool_pair_address)
                self.operatePoolPair()
            else:
                cprint.err("无效的交易对")

    def operatePoolPair(self):
        while True:
            cprint.info(
                f"目前的交易对, Token0: {self.token0_name} / Token1: {self.token1_name}")
            operation = questionary.select("请选择你要的操作：", [
                Choice("查看汇率", "show_rate"),
                Choice("兑换", "exchange"),
                Choice("返回", "back")
            ]).ask()

            if operation == "back":
                return

            elif operation == "show_rate":
                self.getRate()

            elif operation == "exchange":
                self.exchange()

    def getPairData(self, pool_pair_address: str):
        """
        获取交易对信息
        1. 获取交易对的合约
        2. 获取交易对的 token0 和 token1 的合约
        3. 获取交易对的 token0 和 token1 的名称、符号和精度
        """
        cprint.info("切换和获取交易对信息中。。。")
        self.pool_contract = self.w3.eth.contract(
            address=pool_pair_address, abi=self.pool_abi)

        # 获取token0和token1的地址
        self.token0_address = self.pool_contract.functions.token0().call()
        self.token1_address = self.pool_contract.functions.token1().call()

        # 获取token0和token1的合约
        self.token0_contract = self.w3.eth.contract(
            address=self.token0_address, abi=self.erc20_token_abi)
        self.token1_contract = self.w3.eth.contract(
            address=self.token1_address, abi=self.erc20_token_abi)

        # 获取token0和token1的名称
        self.token0_name = self.token0_contract.functions.name().call()
        self.token1_name = self.token1_contract.functions.name().call()

        # 获取token0和token1的符号
        self.token0_symbol = self.token0_contract.functions.symbol().call()
        self.token1_symbol = self.token1_contract.functions.symbol().call()

        # 获取token0和token1的精度
        self.token0_decimals = self.token0_contract.functions.decimals().call()
        self.token1_decimals = self.token1_contract.functions.decimals().call()

        cprint.ok("切换和获取交易对信息完成")

    def getRate(self) -> int:
        # 调用合约的 slot0 函数获取 sqrtPriceX96
        sqrt_price_x96 = self.pool_contract.functions.slot0().call()[0]

        # 计算价格
        # sqrt_price_x96 是价格的平方根，乘以 2^96
        # ETH/USDC 价格计算，因为价格存储为 sqrt(ETH/USDC)，所以要平方后乘以精度因子的倒数
        decimal = max(self.token0_decimals, self.token1_decimals) - \
            min(self.token0_decimals, self.token1_decimals)
        price = (sqrt_price_x96 ** 2 / 2**192) * (10 ** decimal)

        # 打印汇率
        cprint.info(
            f"{self.token0_name}/{self.token1_name} 汇率 [{self.token0_symbol}/{self.token1_symbol}]: {price}")
        
        return sqrt_price_x96

    def exchange(self):
        # DEBUG: 我的测试地址和私钥
        my_address = "0x369c54759Cb1AE18a897ED2c6230Cf2043b92eF9"
        my_private_key = "0x17dbeb53c98904ddf9db33dfc4e37ddb26cd7756b1432362bc85409664b830c3"

        # Recipent Address 默认是自己的地址
        recipient_address = questionary.text("请输入接收地址：", "0xd88032e588EEe73bC3e682be4EcB9B740dfb014a").ask()

        # zeroForOne: true 表示从 token0 兑换成 token1， false 表示从 token1 兑换成 token0
        zero_for_one = questionary.select("请选择兑换方向：", [
            Choice(f"从 {self.token0_name} 兑换成 {self.token1_name}", True),
            Choice(f"从 {self.token1_name} 兑换成 {self.token0_name}", False)
        ]).ask()

        # 显示当前想兑换的 token 余量
        if zero_for_one:
            token_left = self.token0_contract.functions.balanceOf(my_address).call()
            cprint.info(f"当前 {self.token0_name} 余量: {self.token0_contract.functions.balanceOf(my_address).call() / 10 ** self.token0_decimals}")
        else:
            token_left = self.token1_contract.functions.balanceOf(my_address).call()
            cprint.info(f"当前 {self.token1_name} 余量: {self.token1_contract.functions.balanceOf(my_address).call() / 10 ** self.token1_decimals}")

        while True:
            # amountSpecified: 正数表示需要将多少 token0 拿去兑换，负数表示需要获取多少 token1
            amount_specified = questionary.text(f"请输入需要兑换的 {self.token0_name if zero_for_one else self.token1_name} 数量：",
                                            validate=lambda x: True if x.isdigit() else "请输入有效的数量").ask()
            amount_specified = float(amount_specified) * 10 ** (self.token0_decimals if zero_for_one else self.token1_decimals)
            if amount_specified > token_left:
                cprint.err("输入的数量超过余量")
                continue
            else:
                break

        # sqrtPriceLimitX96: 表示价格限制，如果设置为 0，表示不限制
        sqrt_price_limit_x96=questionary.text(f"请输入价格限制：", str(self.getRate()),
                                                lambda x: True if x.isdigit() or x == "0" else "请输入有效的价格限制").ask()

        # data: 可选信息
        data = b''

        # 设置交易参数
        from_address = my_address
        nonce = self.w3.eth.get_transaction_count(from_address)
        gas_price = self.w3.eth.gas_price

        # 创建交易字典
        txn_dict = self.pool_contract.functions.swap(
            recipient_address,
            zero_for_one,
            int(amount_specified),
            int(sqrt_price_limit_x96),
            data
        ).build_transaction({
            'from': from_address,
            'nonce': nonce,
            'gasPrice': gas_price,
            'gas': 200000,
            'chainId': self.w3.eth.chain_id
        })

        # 签署交易
        private_key = my_private_key
        signed_txn = self.w3.eth.account.sign_transaction(txn_dict, private_key=private_key)

        # 发送交易
        tx_receipt = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # 获取交易回执
        print(tx_receipt)
        pass
