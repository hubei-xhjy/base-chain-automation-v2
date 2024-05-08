# EVM 自动化项目开发笔记

## 安全

打开 Main 函数，让用户输入密码。

| 工作目录没有 auth 文件                 | 工作目录有 auth 文件            |
| -------------------------------------- | ------------------------------- |
| 生成 salt 和 iv 然后保存到 auth 文件中 | 读取 auth 文件，获得 salt 和 iv |

用 password + salt 生成密钥，随机生成 IV

将密钥和 IV 暂存到 os.environ 里。

密钥，加上 IV 进行 AES 加密

> auth 文件要进行多次备份，否则一旦文件损坏，则加密文件没有复原的可能

## Main 函数执行逻辑

### 准备工作

1. 准备工作目录，如果没有工作目录，则创建
2. 让用户输入密码，15 位及以上，然后生成 auth 文件
3. 可选择目录
   1. 创建钱包
   2. 生成交互路径（随机进行搭配不同的交互路径）

## 文件结构

### 项目工作目录

```plaintext
$HOME/Documents/gn_automation

/
|-/log
|-/backup
| |- auth_datetime
| |- wallets_datetime.bin
|- auth
|- wallets.bin          # 加密后的 wallets 文件
```
