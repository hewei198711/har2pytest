import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_shoppedGift_deleteProduct(data=data, headers=headers):
    """
    删除活动商品
    /mgmt/prmt/shoppedGift/deleteProduct

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/shoppedGift/deleteProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
