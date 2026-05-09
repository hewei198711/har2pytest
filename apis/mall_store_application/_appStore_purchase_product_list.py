import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchase_product_list(headers=headers):
    """
    可押货商品列表
    /appStore/purchase/product/list
    """

    url = "/appStore/purchase/product/list"
    with client.get(url=url, headers=headers) as r:
        return r
