import os

from util.client import client

data = {
    "idList": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_deleteDisable(data=data, headers=headers):
    """
    删除不派发顾客
    /mgmt/prmt/couponGrant/deleteDisable
    """

    url = "/mgmt/prmt/couponGrant/deleteDisable"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
