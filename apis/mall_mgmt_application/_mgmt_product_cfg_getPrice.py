import os

from util.client import client

headers = {
    "channel": "pc",
    "client": "op",
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_product_cfg_getPrice(headers=headers):
    """
    价格参数查询
    /mgmt/product/cfg/getPrice
    """

    url = "/mgmt/product/cfg/getPrice"
    with client.get(url=url, headers=headers) as r:
        return r
