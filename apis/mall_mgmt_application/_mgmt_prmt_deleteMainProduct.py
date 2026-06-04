import os

from util.client import client

data = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_deleteMainProduct(data=data, headers=headers):
    """
    删除主产品
    /mgmt/prmt/deleteMainProduct

    参数说明:
    - id: id
    """

    url = "/mgmt/prmt/deleteMainProduct"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
