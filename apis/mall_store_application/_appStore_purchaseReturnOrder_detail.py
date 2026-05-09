import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_detail(headers=headers):
    """
    获取退货单详情
    /appStore/purchaseReturnOrder/detail
    """

    url = "/appStore/purchaseReturnOrder/detail"
    with client.get(url=url, headers=headers) as r:
        return r
