import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_searchCartProducts(headers=headers):
    """
    获取购物车数据
    /appStore/store/dis/mortgageOrder/searchCartProducts
    """

    url = "/appStore/store/dis/mortgageOrder/searchCartProducts"
    with client.get(url=url, headers=headers) as r:
        return r
