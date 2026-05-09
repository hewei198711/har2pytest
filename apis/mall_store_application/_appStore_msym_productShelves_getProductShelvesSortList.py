import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_msym_productShelves_getProductShelvesSortList(headers=headers):
    """
    获取线上店铺货架排序列表
    /appStore/msym/productShelves/getProductShelvesSortList
    """

    url = "/appStore/msym/productShelves/getProductShelvesSortList"
    with client.get(url=url, headers=headers) as r:
        return r
