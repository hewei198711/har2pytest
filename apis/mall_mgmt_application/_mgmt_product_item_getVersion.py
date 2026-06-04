import os

from util.client import client

params = {
    "verId": "",  # verId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_item_getVersion(params=params, headers=headers):
    """
    查询商品
    /mgmt/product/item/getVersion

    参数说明:
    - verId: verId
    """

    url = "/mgmt/product/item/getVersion"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
