import os

from util.client import client

data = {
    "data": "",  # 经过AES加密后的短信验证码参数,原始参数参考无加密接口sendSmsCode
    "key": "",  # 经过RSA公钥加密后的AES KEY
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_sendSmsCodeEncrypt(data=data, headers=headers):
    """
    发送短信验证码(加密)
    /appStore/store/sendSmsCodeEncrypt

    参数说明:
    - data: 经过AES加密后的短信验证码参数,原始参数参考无加密接口sendSmsCode
    - key: 经过RSA公钥加密后的AES KEY
    """

    url = "/appStore/store/sendSmsCodeEncrypt"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
