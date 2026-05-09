import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_negateProducts(headers=headers):
    """
    提交押货单页面的负库存押货商品列表
    /appStore/purchaseOrder/negateProducts
    """

    url = "/appStore/purchaseOrder/negateProducts"
    with client.get(url=url, headers=headers) as r:
        return r
