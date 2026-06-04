import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_jump_detail(params=params, headers=headers):
    """
    详情
    /mgmt/product/jump/detail

    参数说明:
    - id: id
    """

    url = "/mgmt/product/jump/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
