import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_purchaseOrder_pushProductsToCart(headers=headers):
    """
    推送购物车数据
    /appStore/purchaseOrder/pushProductsToCart
    """

    url = "/appStore/purchaseOrder/pushProductsToCart"
    with client.post(url=url, headers=headers) as r:
        return r
