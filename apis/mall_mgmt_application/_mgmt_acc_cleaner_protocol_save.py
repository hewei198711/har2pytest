import os

from util.client import client

data = {
    "protocol": "",  # 协议内容
    "protocolName": "",  # 协议名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_acc_cleaner_protocol_save(data=data, headers=headers):
    """
    保存清洗人协议
    /mgmt/acc/cleaner/protocol/save

    参数说明:
    - protocol: 协议内容
    - protocolName: 协议名称
    """

    url = "/mgmt/acc/cleaner/protocol/save"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
