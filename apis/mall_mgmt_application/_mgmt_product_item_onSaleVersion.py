import os
from urllib.parse import urlencode

from util.client import client

data = {
    "productId": "",  # productId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_product_item_onSaleVersion(data=data, headers=headers):
    """
    商品版本上架
    /mgmt/product/item/onSaleVersion

    参数说明:
    - productId: productId
    """

    url = "/mgmt/product/item/onSaleVersion"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
