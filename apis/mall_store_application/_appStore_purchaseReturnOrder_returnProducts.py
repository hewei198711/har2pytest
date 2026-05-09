import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_returnProducts(headers=headers):
    """
    提交退货单页面的押货退货商品搜索
    /appStore/purchaseReturnOrder/returnProducts
    """

    url = "/appStore/purchaseReturnOrder/returnProducts"
    with client.get(url=url, headers=headers) as r:
        return r
