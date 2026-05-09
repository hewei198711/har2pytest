import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_returnOrder_searchPositiveProducts(headers=headers):
    """
    获取服务中心正库存的商品信息
    /appStore/store/dis/mortgage/returnOrder/searchPositiveProducts
    """

    url = "/appStore/store/dis/mortgage/returnOrder/searchPositiveProducts"
    with client.get(url=url, headers=headers) as r:
        return r
