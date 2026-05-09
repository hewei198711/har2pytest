import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_products(headers=headers):
    """
    提交押货单页面的押货商品搜索
    /appStore/purchaseOrder/products
    """

    url = "/appStore/purchaseOrder/products"
    with client.get(url=url, headers=headers) as r:
        return r
