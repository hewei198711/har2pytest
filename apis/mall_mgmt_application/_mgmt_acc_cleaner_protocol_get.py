import os

from util.client import client

params = {
    "protocolName": "",  # 协议名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_cleaner_protocol_get(params=params, headers=headers):
    """
    根据名称获取协议信息
    /mgmt/acc/cleaner/protocol/get

    参数说明:
    - protocolName: 协议名称
    """

    url = "/mgmt/acc/cleaner/protocol/get"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
