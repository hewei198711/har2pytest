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


def _mgmt_prmt_couponGrant_deleteUserByCardNo(data=data, headers=headers):
    """
    根据会员卡号删除派发会员
    /mgmt/prmt/couponGrant/deleteUserByCardNo

    参数说明:
    - cardNo: 会员卡号
    - code: 门店编号
    - id: id
    """

    url = "/mgmt/prmt/couponGrant/deleteUserByCardNo"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
