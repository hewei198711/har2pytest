import os
from urllib.parse import urlencode

from util.client import client

data = {
    "ids": [],  # ids
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_item_batchDel(data=data, headers=headers):
    """
    商品版本删除
    /mgmt/product/item/batchDel

    参数说明:
    - ids: ids
    """

    url = "/mgmt/product/item/batchDel"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
