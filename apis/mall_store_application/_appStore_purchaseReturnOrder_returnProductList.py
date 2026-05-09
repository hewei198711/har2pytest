import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_returnProductList(headers=headers):
    """
    获取所有的押货退货商品信息
    /appStore/purchaseReturnOrder/returnProductList
    """

    url = "/appStore/purchaseReturnOrder/returnProductList"
    with client.get(url=url, headers=headers) as r:
        return r
