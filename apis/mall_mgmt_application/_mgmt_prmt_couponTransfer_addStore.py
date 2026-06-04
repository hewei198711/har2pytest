import os

from util.client import client

data = {
    "code": "",  # 门店编号
    "grantCount": 0,  # 派发数量
    "grantId": 0,  # 派发id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_addStore(data=data, headers=headers):
    """
    手动新增派发顾客
    /mgmt/prmt/couponTransfer/addStore

    参数说明:
    - code: 门店编号
    - grantCount: 派发数量
    - grantId: 派发id
    """

    url = "/mgmt/prmt/couponTransfer/addStore"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
