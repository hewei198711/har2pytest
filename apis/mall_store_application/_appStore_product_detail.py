import os

from util.client import client

params = {
    "productId": "",  # productId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_product_detail(params=params, headers=headers):
    """
    产品详情
    /appStore/product/detail

    参数说明:
    - productId: productId
    """

    url = "/appStore/product/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
