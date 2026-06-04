import os

from util.client import client

data = {
    "id": 0,  # 派发id
    "remarks": "",  # 备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_stopGrant(data=data, headers=headers):
    """
    停止派发
    /mgmt/prmt/couponGrant/stopGrant

    参数说明:
    - id: 派发id
    - remarks: 备注
    """

    url = "/mgmt/prmt/couponGrant/stopGrant"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
