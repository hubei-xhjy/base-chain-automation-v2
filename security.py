import os
import questionary
from config import AUTH_FILE, VERIFY_FILE, OS_PASSWD
from src.crypto.aes import derive_key, encrypt as aes_encrypt, decrypt as aes_decrypt
from cprint import cprint

VERIFY_CONTENT = "this_password_passed_the_verify"


def verify_password_retype(password: str, re_password: str):
    if password == re_password:
        return True
    else:
        return False
    

def verify_password(password: str):
    salt, iv = get_auth()
    key = derive_key(password, salt)
    with open(VERIFY_FILE, 'rb') as f:
        content = f.read()
        try:
            verify_content = aes_decrypt(content, key, iv)
            if verify_content == VERIFY_CONTENT:
                return True
            else:
                return False
        except Exception:
            return False


def setup():
    # 如果 auth 文件不存在，且内容为空，则表示是老用户
    if not os.path.exists(VERIFY_FILE) or os.path.getsize(VERIFY_FILE) == 0:
        password = questionary.password("请输入密码，强度在 15 位及以上：",
                                        validate=lambda pwd: True if len(pwd) >= 15 else '密码强度不够').ask()
        if password == None:
            exit()

        for attempt in range(3):
            re_password = questionary.password("请输入密码：").ask()
            if re_password == None:
                exit()

            if verify_password_retype(password, re_password):
                break

            else:
                cprint.warn("密码不一致，请重新输入！")
            
            if attempt == 2:
                cprint.err("密码输入错误次数过多，请重新登录！")
                exit()
        
        # 将文本加密后保存，作为验证
        salt, iv = get_auth()
        key = derive_key(password, salt)
        with open(VERIFY_FILE, 'wb') as f:
            f.write(aes_encrypt(VERIFY_CONTENT, key, iv))

    else:
        # 如果是老用户，则只需要输入密码
        for attempt in range(3):
            password = questionary.password("请输入密码：").ask()
            if password == None:
                exit()
            
            # 拿上面事先保存好的文本来解密，成功就能进入系统
            if verify_password(password):
                break
            else:
                cprint.warn("密码错误，请重新输入！")
            
            if attempt == 2:
                cprint.err("密码输入错误次数过多，请重新登录！")
                exit()
    
    os.environ.setdefault(OS_PASSWD, password)


def get_auth():
    if not os.path.exists(AUTH_FILE) or os.path.getsize(AUTH_FILE) == 0:
        with open(AUTH_FILE, 'wb') as f:
            salt = os.urandom(16)
            iv = os.urandom(16)
            f.writelines([salt, iv])
            cprint.info("已生成加密文件，请勿删除，并做好备份！")
    else:
        with open(AUTH_FILE, 'rb') as f:
            salt = f.read(16)
            iv = f.read(16)

    return salt, iv


def encrypt(data):
    salt, iv = get_auth()
    key = derive_key(os.environ.get(OS_PASSWD), salt)
    return aes_encrypt(data, key, iv)


def decrypt(data):
    salt, iv = get_auth()
    key = derive_key(os.environ.get(OS_PASSWD), salt)
    return aes_decrypt(data, key, iv)