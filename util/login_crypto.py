"""
登录参数加密工具
功能：使用 AES + RSA 加密登录参数，生成安全传输的数据包
"""

import base64
import json

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA

# 常量定义
AES_KEY = "HFLkbvwm015UkdrD"  # AES-128 密钥（16字节）
RSA_PUBLIC_KEY = (
    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDf3n7GvYCjevA+JEnMQHfxDX/ePSv"
    "iRR2C2tsNSVyuTm6TfaP/HLzNbAO0kK+52nr2HO2LzsSd+a98V4n5npYDWPqbswXzKLj73k"
    "BlBI0P6Uf3uygCAZtfd9qkAn0DkgGpVw1VtCb33svBkaQinOYB550OygDM1vemuQYq11E/mQIDAQAB"
)


def _pad_to_block_size(data: str) -> bytes:
    """
    对字符串进行填充，使其长度为 16 的倍数（AES块对齐）
    :param data: 待填充的字符串
    :return: 填充后的字节数据
    """
    pad_len = 16 - len(data) % 16
    padding = chr(pad_len) * pad_len
    return (data + padding).encode("utf-8")


def aes_encrypt(plaintext: str, key: str, mode=AES.MODE_ECB) -> str:
    """
    使用 AES 加密字符串数据
    :param plaintext: 明文数据（字符串）
    :param key: AES 密钥（16/24/32字节）
    :param mode: 加密模式（默认ECB）
    :return: Base64编码的密文
    """
    cipher = AES.new(key.encode("utf-8"), mode)
    padded_data = _pad_to_block_size(plaintext)
    encrypted_bytes = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_bytes).decode("utf-8").replace("\n", "")


def _format_rsa_public_key(rsa_key: str) -> str:
    """
    格式化RSA公钥为PEM标准格式
    :param rsa_key: 原始公钥字符串
    :return: 带PEM头尾的标准公钥
    """
    start = "-----BEGIN PUBLIC KEY-----\n"
    end = "-----END PUBLIC KEY-----"
    formatted_key = ""

    # 每64字符换行
    for i in range(0, len(rsa_key), 64):
        formatted_key += rsa_key[i : i + 64] + "\n"

    return start + formatted_key + end


def rsa_encrypt(plaintext: str, public_key: str) -> str:
    """
    使用RSA公钥加密数据（PKCS#1 v1.5）
    :param plaintext: 待加密字符串
    :param public_key: PEM格式RSA公钥
    :return: Base64编码的加密结果
    """
    try:
        formatted_key = _format_rsa_public_key(public_key)
        pub_key = RSA.import_key(formatted_key)
        cipher = PKCS1_v1_5.new(pub_key)
        encrypted_bytes = cipher.encrypt(plaintext.encode("utf-8"))

        if not encrypted_bytes:
            raise RuntimeError("RSA加密失败：返回空结果")

        return base64.b64encode(encrypted_bytes).decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"RSA加密失败: {e}")


def encrypt_login_params(username: str, password: str, channel: str = "", phone_no: str = "") -> dict:
    """
    加密登录参数
    :param username: 用户名
    :param password: 密码
    :param channel: 渠道类型（op/store/shortcut）
    :param phone_no: 手机号（shortcut渠道必需）
    :return: 包含加密数据的字典 {data: AES密文, key: RSA加密的AES密钥}
    """
    try:
        # 构造请求参数
        payload = {"username": username, "password": password, "grant_type": "password"}

        # 添加渠道特定参数
        if channel == "store":
            payload["auth_type"] = "store"
        elif channel == "op":
            payload["auth_type"] = "op"
        elif channel == "shortcut":
            payload.update({"auth_type": "shortcut", "phoneNo": phone_no})

        # 序列化并加密
        json_str = json.dumps(payload)
        encrypted_data = aes_encrypt(json_str, AES_KEY)
        encrypted_key = rsa_encrypt(AES_KEY, RSA_PUBLIC_KEY)

        return {"data": encrypted_data, "key": encrypted_key}
    except Exception as e:
        raise RuntimeError(f"登录参数加密失败: {e}")
