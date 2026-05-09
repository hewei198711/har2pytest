import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgageOrder_searchNegativeProducts(headers=headers):
    """
    查询店铺所有所有负库存的商品
    /appStore/store/dis/mortgageOrder/searchNegativeProducts
    """

    url = "/appStore/store/dis/mortgageOrder/searchNegativeProducts"
    with client.get(url=url, headers=headers) as r:
        return r
