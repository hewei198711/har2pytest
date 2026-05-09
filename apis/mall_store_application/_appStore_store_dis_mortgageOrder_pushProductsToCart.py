import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _appStore_store_dis_mortgageOrder_pushProductsToCart(headers=headers):
    """
    推送购物车数据
    /appStore/store/dis/mortgageOrder/pushProductsToCart
    """

    url = "/appStore/store/dis/mortgageOrder/pushProductsToCart"
    with client.post(url=url, headers=headers) as r:
        return r
