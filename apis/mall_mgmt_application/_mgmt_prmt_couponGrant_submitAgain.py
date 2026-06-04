import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_couponGrant_submitAgain(data=data, headers=headers):
    """
    再次提交派发记录
    /mgmt/prmt/couponGrant/submitAgain

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/couponGrant/submitAgain"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
