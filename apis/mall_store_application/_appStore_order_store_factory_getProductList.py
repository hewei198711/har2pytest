import os

from util.client import client

params = {
    "keyword": "",  # keyword
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_order_store_factory_getProductList(params=params, headers=headers):
    """
    根据关键字模糊查询商品信息
    /appStore/order/store/factory/getProductList

    参数说明:
    - keyword: keyword
    """

    url = "/appStore/order/store/factory/getProductList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
