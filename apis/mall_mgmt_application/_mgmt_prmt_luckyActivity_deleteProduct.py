import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_luckyActivity_deleteProduct(data=data, headers=headers):
    """
    手动删除活动黑名单产品
    /mgmt/prmt/luckyActivity/deleteProduct

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/luckyActivity/deleteProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
