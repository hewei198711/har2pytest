import os
from urllib.parse import urlencode

from util.client import client

data = {
    "verId": "",  # verId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_item_revertVersion(data=data, headers=headers):
    """
    商品版本撤回
    /mgmt/product/item/revertVersion

    参数说明:
    - verId: verId
    """

    url = "/mgmt/product/item/revertVersion"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
