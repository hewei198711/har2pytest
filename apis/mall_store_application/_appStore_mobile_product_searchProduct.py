import os

from util.client import client

params = {
    "product": "",  # product
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_mobile_product_searchProduct(params=params, headers=headers):
    """
    产品精确编号或模糊名称搜索
    /appStore/mobile/product/searchProduct

    参数说明:
    - product: product
    """

    url = "/appStore/mobile/product/searchProduct"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
