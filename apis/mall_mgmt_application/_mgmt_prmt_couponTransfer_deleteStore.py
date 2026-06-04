import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "code": "",  # 门店编号
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponTransfer_deleteStore(data=data, headers=headers):
    """
    删除导入门店
    /mgmt/prmt/couponTransfer/deleteStore

    参数说明:
    - cardNo: 会员卡号
    - code: 门店编号
    - id: id
    """

    url = "/mgmt/prmt/couponTransfer/deleteStore"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
