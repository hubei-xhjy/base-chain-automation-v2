import configparser
import os
import pathlib
import random

config = configparser.ConfigParser()
config.read(".conf")

HOME_PATH = pathlib.Path.home()

PROJECT_DIR = os.path.join(HOME_PATH, config['DEFAULT']['project_dir'])
LOG_DIR = os.path.join(HOME_PATH, config['DEFAULT']['log_dir'])
WALLET_DIR = os.path.join(HOME_PATH, config['DEFAULT']['wallet_dir'])
WALLET_BACKUP_DIR = os.path.join(HOME_PATH, config['DEFAULT']['wallet_backup_dir'])

AUTH_FILE = os.path.join(HOME_PATH, config['DEFAULT']['auth_file'])
VERIFY_FILE = os.path.join(HOME_PATH, config['DEFAULT']['verify_file'])

# OS Environment Key
OS_PASSWD = "gn_password"
OS_IV = "gn_iv"

def setup():
    # Create directory if not exists
    if not os.path.exists(PROJECT_DIR):
        os.mkdir(PROJECT_DIR)
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    if not os.path.exists(WALLET_DIR):
        os.mkdir(WALLET_DIR)
    if not os.path.exists(WALLET_BACKUP_DIR):
        os.mkdir(WALLET_BACKUP_DIR)

# BASE 
BASE_RPC_LIST = [
    "https://base.llamarpc.com",
    "https://base-pokt.nodies.app",
    "https://mainnet.base.org",
    "https://developer-access-mainnet.base.org",
    # "https://base-mainnet.diamondswap.org/rpc",
    "https://base.blockpi.network/v1/rpc/public",
    "https://1rpc.io/base",
    "https://base-pokt.nodies.app",
    "https://base.meowrpc.com",
    "https://base-mainnet.public.blastapi.io",
    "https://base.gateway.tenderly.co"
]

def getBaseRpc() -> str:
    return random.choice(BASE_RPC_LIST)