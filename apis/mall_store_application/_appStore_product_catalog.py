import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_product_catalog(headers=headers):
    """
    产品分类
    /appStore/product/catalog
    """

    url = "/appStore/product/catalog"
    with client.get(url=url, headers=headers) as r:
        return r
