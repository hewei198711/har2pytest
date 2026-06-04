import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_deleteProduct(data=data, headers=headers):
    """
    删除产品
    /mgmt/prmt/deleteProduct

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/deleteProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
