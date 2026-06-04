import os

from util.client import client

data = {
    "email": "",  # 通知接收邮件
    "newAddress": "",  # 新的收货地址
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_sendAddressChangeMsg(data=data, headers=headers):
    """
    服务中心收货地址发生变更发送邮件消息
    /mgmt/store/sendAddressChangeMsg

    参数说明:
    - email: 通知接收邮件
    - newAddress: 新的收货地址
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/sendAddressChangeMsg"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
