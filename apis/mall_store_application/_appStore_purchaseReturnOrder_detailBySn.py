import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseReturnOrder_detailBySn(headers=headers):
    """
    SN获取退货单详情
    /appStore/purchaseReturnOrder/detailBySn
    """

    url = "/appStore/purchaseReturnOrder/detailBySn"
    with client.get(url=url, headers=headers) as r:
        return r
