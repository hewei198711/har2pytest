import os

from util.client import client

params = {
    "productCode": "",  # productCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchase_product(params=params, headers=headers):
    """
    获取商品信息
    /appStore/purchase/product

    参数说明:
    - productCode: productCode
    """

    url = "/appStore/purchase/product"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
