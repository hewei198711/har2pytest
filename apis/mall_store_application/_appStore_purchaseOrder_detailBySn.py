import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_purchaseOrder_detailBySn(headers=headers):
    """
    SN获取押货单详情
    /appStore/purchaseOrder/detailBySn
    """

    url = "/appStore/purchaseOrder/detailBySn"
    with client.get(url=url, headers=headers) as r:
        return r
